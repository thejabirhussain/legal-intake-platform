from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.all_models import Conversation, Message, Client, Case, CaseStatus, MessageSender
from app.services.llm_service import llm_service
from app.services.whatsapp_service import whatsapp_service
import json

class IntakeAgent:
    async def process_message(self, db: AsyncSession, from_phone: str, message_content: str, message_type: str = "text"):
        """
        Main entry point for processing an incoming user message.
        """
        # 1. Identify Client
        result = await db.execute(select(Client).filter(Client.phone_number == from_phone))
        client = result.scalars().first()
        
        if not client:
            client = Client(phone_number=from_phone)
            db.add(client)
            await db.commit()
            await db.refresh(client)

        # 2. Get Active Case/Conversation
        # Simplified: Assume one active case per client for now, or create new if none exist
        # In production, check for most recent active intake
        result = await db.execute(
            select(Case).filter(Case.client_id == client.id, Case.status == CaseStatus.INTAKE_IN_PROGRESS)
        )
        case = result.scalars().first()

        if not case:
            case = Case(client_id=client.id, status=CaseStatus.INTAKE_IN_PROGRESS)
            db.add(case)
            await db.commit()
            await db.refresh(case)
            
            conversation = Conversation(case_id=case.id, state="START")
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)
        else:
            result = await db.execute(select(Conversation).filter(Conversation.case_id == case.id))
            conversation = result.scalars().first()

        # 3. Save User Message
        user_msg = Message(
            conversation_id=conversation.id,
            content=message_content,
            sender=MessageSender.USER,
            message_type=message_type
        )
        db.add(user_msg)
        await db.commit()

        # 4. State Machine Logic
        current_state = conversation.state
        next_state = current_state
        ai_response_text = ""

        # --- STATE: START ---
        if current_state == "START":
            # Just starting, ask for name if not known, or what help they need
            if not client.name:
                ai_response_text = "Welcome to Smart Lawyer Assistant. Before we begin, may I ask for your full name?"
                next_state = "IDENTIFY_CLIENT"
            else:
                ai_response_text = f"Hello {client.name}. How can I assist you with your legal matter today? Please briefly describe your situation."
                next_state = "DETERMINE_CASE_TYPE"
        
        # --- STATE: IDENTIFY_CLIENT ---
        elif current_state == "IDENTIFY_CLIENT":
            # User provided name
            client.name = message_content
            db.add(client)
            ai_response_text = f"Thank you, {client.name}. Could you please describe your legal issue or what happened?"
            next_state = "DETERMINE_CASE_TYPE"

        # --- STATE: DETERMINE_CASE_TYPE ---
        elif current_state == "DETERMINE_CASE_TYPE":
            # Use LLM to classify case type
            system_prompt = "Classify this legal issue into one of: 'Personal Injury', 'Family Law', 'Criminal Defense', 'Corporate', 'Other'. Return JSON: {'case_type': '...', 'urgency': 'High/Medium/Low'}"
            # Use Ollama for simpler extraction tasks to save cost/latency if desired, or OpenAI for better accuracy.
            # Here we default to OpenAI for accuracy but you can switch to use_local=True
            extraction = await llm_service.extract_structured_data(message_content, {"case_type": "string", "urgency": "string"}, use_local=True)
            
            case.case_type = extraction.get("case_type", "Other")
            case.urgency = extraction.get("urgency", "Medium")
            db.add(case)
            
            ai_response_text = f"I understand this is a {case.case_type} matter (Urgency: {case.urgency}). To better assess your case, I need to ask a few detailed questions. First, when did this incident occur?"
            next_state = "COLLECT_DETAILS_TIME"

        # --- STATE: COLLECT_DETAILS_TIME ---
        elif current_state == "COLLECT_DETAILS_TIME":
            # Save time info to context (simplified)
            context = conversation.context_data or {}
            context["incident_time"] = message_content
            conversation.context_data = context
            
            ai_response_text = "Thank you. Can you please provide any specific details about the parties involved?"
            next_state = "COLLECT_DETAILS_PARTIES"
        
        # --- STATE: COLLECT_DETAILS_PARTIES ---
        elif current_state == "COLLECT_DETAILS_PARTIES":
            context = conversation.context_data or {}
            context["parties"] = message_content
            conversation.context_data = context
            
            ai_response_text = "Got it. Do you have any documents or photos related to this? You can upload them here, or type 'no' to proceed."
            next_state = "COLLECT_DOCS"

        # --- STATE: COLLECT_DOCS ---
        elif current_state == "COLLECT_DOCS":
            # If they uploaded media, it would be handled (logic simplified here)
            if message_type != "text" or "no" not in message_content.lower():
                ai_response_text = "Thank you for the documents. I have gathered the initial information. I will now generate a summary for our lawyers to review. Is there anything else you'd like to add?"
            else:
                ai_response_text = "Understood. I have gathered the initial information. Is there anything else you'd like to add before I submit this for review?"
            next_state = "FINAL_CHECK"

        # --- STATE: FINAL_CHECK ---
        elif current_state == "FINAL_CHECK":
            ai_response_text = "Thank you. Your case intake has been submitted to a Senior Lawyer for review. We will contact you shortly with next steps."
            next_state = "COMPLETE"
            case.status = CaseStatus.PENDING_REVIEW
            
            # Generate Summary
            summary_prompt = "Summarize this legal intake case based on the conversation."
            # Use OpenAI for high-quality summarization
            case.summary = await llm_service.generate_response(summary_prompt, f"Client: {client.name}, Type: {case.case_type}, Details: {json.dumps(conversation.context_data)}", use_local=False)
            db.add(case)

        # --- STATE: COMPLETE ---
        elif current_state == "COMPLETE":
             ai_response_text = "Your case is already under review. We will get back to you soon."
        
        
        # 5. Update State & Send Response
        conversation.state = next_state
        db.add(conversation)
        
        agent_msg = Message(
            conversation_id=conversation.id,
            content=ai_response_text,
            sender=MessageSender.AGENT,
            message_type=MessageType.TEXT
        )
        db.add(agent_msg)
        await db.commit()

        # 6. Send to WhatsApp
        await whatsapp_service.send_text_message(from_phone, ai_response_text)

intake_agent = IntakeAgent()

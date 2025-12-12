"""
AI Services Module for SwissAxa Portal
Handles all AI-powered features using OpenAI API
"""
import os
import json
from typing import Dict, List, Optional
from openai import OpenAI
from datetime import datetime

# Initialize OpenAI client
openai_client = None
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


class AIService:
    """Main AI service class for handling all AI operations"""
    
    @staticmethod
    def is_available() -> bool:
        """Check if AI services are available"""
        return openai_client is not None
    
    @staticmethod
    def compare_policies(external_policy_data: Dict) -> Dict:
        """
        Compare external policy with SwissAxa products using AI
        """
        if not AIService.is_available():
            # Fallback to mock data
            return AIService._mock_policy_comparison(external_policy_data)
        
        try:
            prompt = f"""
            Analyze this external insurance policy and compare it with SwissAxa insurance products:
            
            Policy Type: {external_policy_data.get('policy_type', 'Unknown')}
            Coverage: {external_policy_data.get('coverage', 'Unknown')}
            Premium: {external_policy_data.get('premium', 'Unknown')}
            Insurance Company: {external_policy_data.get('insurance_company', 'Unknown')}
            
            Provide:
            1. Similar SwissAxa products with match scores (0-100%)
            2. Key differences and advantages of SwissAxa products
            3. Recommendations for the customer
            
            Format as JSON with 'similar_products' (array) and 'recommendations' (array).
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an insurance comparison expert. Provide detailed, accurate comparisons."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content
            
            # Try to parse JSON from response
            try:
                result = json.loads(result_text)
            except:
                # If not JSON, create structured response
                result = {
                    'similar_products': [
                        {
                            'name': 'Comprehensive Insurance Premium',
                            'coverage': external_policy_data.get('policy_type', 'General'),
                            'premium': '99.99 EUR/month',
                            'match_score': 85,
                            'ai_analysis': result_text[:200]
                        }
                    ],
                    'recommendations': result_text.split('\n')[:5]
                }
            
            return result
            
        except Exception as e:
            print(f"AI Policy Comparison Error: {e}")
            return AIService._mock_policy_comparison(external_policy_data)
    
    @staticmethod
    def _mock_policy_comparison(external_policy_data: Dict) -> Dict:
        """Mock policy comparison when AI is not available"""
        return {
            'similar_products': [
                {
                    'name': 'Comprehensive Insurance Premium',
                    'coverage': external_policy_data.get('policy_type', 'General'),
                    'premium': '99.99 EUR/month',
                    'match_score': 85
                }
            ],
            'recommendations': [
                'Our premium product offers 20% better coverage',
                'Includes 24/7 customer support',
                'Faster claims processing'
            ]
        }
    
    @staticmethod
    def tag_document(filename: str, file_content: Optional[bytes] = None) -> str:
        """
        Auto-tag document type using AI
        Returns: document type tag
        """
        if not AIService.is_available():
            # Fallback: guess from filename
            filename_lower = filename.lower()
            if 'policy' in filename_lower:
                return 'policy'
            elif 'claim' in filename_lower:
                return 'claim'
            elif 'invoice' in filename_lower or 'bill' in filename_lower:
                return 'invoice'
            elif 'report' in filename_lower:
                return 'report'
            elif 'id' in filename_lower or 'passport' in filename_lower:
                return 'identity'
            elif 'medical' in filename_lower or 'doctor' in filename_lower:
                return 'medical'
            else:
                return 'general'
        
        try:
            prompt = f"""
            Analyze this document filename and determine its type:
            Filename: {filename}
            
            Classify it as one of: policy, claim, invoice, report, identity, medical, proof_of_ownership, repair_invoice, police_report, or general.
            
            Return only the classification word.
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a document classification expert. Classify documents accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            tag = response.choices[0].message.content.strip().lower()
            
            # Validate tag
            valid_tags = ['policy', 'claim', 'invoice', 'report', 'identity', 'medical', 
                         'proof_of_ownership', 'repair_invoice', 'police_report', 'general']
            if tag not in valid_tags:
                return 'general'
            
            return tag
            
        except Exception as e:
            print(f"AI Document Tagging Error: {e}")
            return 'general'
    
    @staticmethod
    def analyze_claim_damage(image_description: str = None, claim_description: str = None) -> Dict:
        """
        Analyze claim damage from description and/or images
        Returns: damage_type, severity, estimated_value, priority
        """
        if not AIService.is_available():
            return {
                'damage_type': 'General Damage',
                'severity': 'medium',
                'estimated_value': 0,
                'priority': 'normal',
                'suggested_description': claim_description or 'Damage claim'
            }
        
        try:
            prompt = f"""
            Analyze this insurance claim:
            Description: {claim_description or 'No description provided'}
            Image Analysis: {image_description or 'No image analysis available'}
            
            Provide:
            1. Damage type (water, fire, theft, collision, vandalism, natural_disaster, other)
            2. Severity (low, medium, high, critical)
            3. Estimated claim value range (in EUR)
            4. Priority (urgent, normal, low)
            5. Suggested detailed description
            
            Return as JSON with keys: damage_type, severity, estimated_value_min, estimated_value_max, priority, suggested_description
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an insurance claims assessment expert. Analyze damage accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            
            try:
                result = json.loads(result_text)
            except:
                # Parse from text if not JSON
                result = {
                    'damage_type': 'General Damage',
                    'severity': 'medium',
                    'estimated_value_min': 500,
                    'estimated_value_max': 2000,
                    'priority': 'normal',
                    'suggested_description': result_text[:200] if result_text else claim_description
                }
            
            return result
            
        except Exception as e:
            print(f"AI Claims Analysis Error: {e}")
            return {
                'damage_type': 'General Damage',
                'severity': 'medium',
                'estimated_value_min': 0,
                'estimated_value_max': 0,
                'priority': 'normal',
                'suggested_description': claim_description or 'Damage claim'
            }
    
    @staticmethod
    def recommend_policies(user_profile: Dict) -> List[Dict]:
        """
        Recommend policies based on user profile
        """
        if not AIService.is_available():
            return []
        
        try:
            prompt = f"""
            Based on this customer profile, recommend relevant insurance add-ons or policy upgrades:
            
            Current Policies: {user_profile.get('policies', [])}
            Claims History: {user_profile.get('claims_count', 0)} claims
            Location: {user_profile.get('location', 'Unknown')}
            Age: {user_profile.get('age', 'Unknown')}
            
            Suggest 3-5 relevant insurance products or add-ons with brief explanations.
            Return as JSON array with: name, type, reason, estimated_premium
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an insurance advisor. Provide personalized recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            result_text = response.choices[0].message.content
            
            try:
                recommendations = json.loads(result_text)
                if isinstance(recommendations, list):
                    return recommendations
                else:
                    return [recommendations]
            except:
                return []
                
        except Exception as e:
            print(f"AI Policy Recommendations Error: {e}")
            return []
    
    @staticmethod
    def suggest_appointment_times(user_id: int, appointment_type: str) -> List[str]:
        """
        Suggest optimal appointment times based on patterns
        """
        if not AIService.is_available():
            return []
        
        try:
            prompt = f"""
            Suggest 5 optimal appointment times for {appointment_type} appointments.
            Consider typical agent availability patterns and customer preferences.
            
            Return as JSON array of suggested times in format: ["YYYY-MM-DD HH:MM", ...]
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a scheduling assistant. Suggest optimal appointment times."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content
            
            try:
                times = json.loads(result_text)
                return times if isinstance(times, list) else []
            except:
                return []
                
        except Exception as e:
            print(f"AI Appointment Suggestions Error: {e}")
            return []
    
    @staticmethod
    def detect_transaction_anomaly(transactions: List[Dict]) -> Dict:
        """
        Detect unusual transaction patterns
        """
        if not AIService.is_available() or len(transactions) < 3:
            return {'is_anomaly': False, 'reason': ''}
        
        try:
            prompt = f"""
            Analyze these recent transactions for unusual patterns:
            {json.dumps(transactions[-10:], indent=2)}
            
            Detect if there are anomalies (unusual amounts, frequencies, patterns).
            Return JSON with: is_anomaly (boolean), reason (string), risk_level (low/medium/high)
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a fraud detection expert. Identify suspicious transaction patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content
            
            try:
                return json.loads(result_text)
            except:
                return {'is_anomaly': False, 'reason': '', 'risk_level': 'low'}
                
        except Exception as e:
            print(f"AI Transaction Analysis Error: {e}")
            return {'is_anomaly': False, 'reason': '', 'risk_level': 'low'}
    
    @staticmethod
    def validate_user_data(user_data: Dict) -> Dict:
        """
        Validate user data for inconsistencies
        """
        if not AIService.is_available():
            return {'is_valid': True, 'inconsistencies': []}
        
        try:
            prompt = f"""
            Check this user data for inconsistencies:
            Name: {user_data.get('first_name')} {user_data.get('last_name')}
            Address: {user_data.get('address')}
            Correspondence Address: {user_data.get('correspondence_address')}
            Phone: {user_data.get('phone')}
            Email: {user_data.get('email')}
            
            Check for:
            - Address format issues
            - Phone number format issues
            - Inconsistencies between addresses
            - Identity mismatches
            
            Return JSON with: is_valid (boolean), inconsistencies (array of strings), requires_reauth (boolean)
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a data validation expert. Check for inconsistencies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content
            
            try:
                return json.loads(result_text)
            except:
                return {'is_valid': True, 'inconsistencies': [], 'requires_reauth': False}
                
        except Exception as e:
            print(f"AI Data Validation Error: {e}")
            return {'is_valid': True, 'inconsistencies': [], 'requires_reauth': False}
    
    @staticmethod
    def chat_with_ai(message: str, conversation_history: List[Dict] = None) -> str:
        """
        Chat with AI assistant
        """
        if not AIService.is_available():
            return "AI services are currently unavailable. Please contact customer service for assistance."
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful customer service assistant for SwissAxa Insurance. 
                    You can help with:
                    - Policy questions
                    - Claims information
                    - Document requirements
                    - General insurance inquiries
                    
                    Be friendly, professional, and concise. If you cannot answer something, direct the customer to contact support."""
                }
            ]
            
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Last 5 messages for context
            
            messages.append({"role": "user", "content": message})
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI Chat Error: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again or contact customer service."


# import json
# import yaml
# import os
from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from models.ollama_models import OllamaModel, OllamaJSONModel
from models.vllm_models import VllmJSONModel, VllmModel
from models.groq_models import GroqModel, GroqJSONModel
from models.claude_models import ClaudModel, ClaudJSONModel
from models.gemini_models import GeminiModel, GeminiJSONModel
from prompts.prompts import (
    planning_agent_prompt,
    integration_agent_prompt,
    check_response_prompt,
    check_response_json,
    generate_searches_prompt,
    get_search_page_prompt

)
from utils.helper_functions import get_current_utc_datetime, check_for_content

class Agent:
    def __init__(self, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        if self.server == 'ollama':
            return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(model=self.model, temperature=self.temperature)
        if self.server == 'vllm':
            return VllmJSONModel(
                model=self.model, 
                guided_json=self.guided_json,
                stop=self.stop,
                model_endpoint=self.model_endpoint,
                temperature=self.temperature
            ) if json_model else VllmModel(
                model=self.model,
                model_endpoint=self.model_endpoint,
                stop=self.stop,
                temperature=self.temperature
            )
        if self.server == 'groq':
            return GroqJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GroqModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'claude':
            return ClaudJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else ClaudModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'gemini':
            return GeminiJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model=self.model,
                temperature=self.temperature
            )      

    
class PlannerAgent(Agent):
    def invoke(self, query,plan=None, prompt=planning_agent_prompt, feedback=None):
       

        planner_prompt = prompt.format(
                plan=plan,
                feedback=feedback,
                datetime=get_current_utc_datetime(),
            )

        messages = [
            {"role": "system", "content": planner_prompt},
            {"role": "user", "content": f"research question: {query}"}
        ]
        llm = self.get_llm(json_model=False)
        ai_msg = llm.invoke(messages)
        response = ai_msg

        print(colored(f"PlannerAgent 👩🏿‍💻: {response}", 'cyan'))
        return response
    
class IntegrationAgent(Agent):
    def invoke(self, query, plan, outputs, reason, previous_response, prompt=integration_agent_prompt):
      
        planner_prompt = prompt.format(
                outputs=outputs,
                plan=plan,
                reason=reason,
                sources=outputs.get('sources', ''),
                previous_response=previous_response,
                datetime=get_current_utc_datetime(),
            )

        messages = [
            {"role": "system", "content": planner_prompt},
            {"role": "user", "content": f"research question: {query}"}
        ]

        llm = self.get_llm(json_model=False)
        ai_msg = llm.invoke(messages)
        response = ai_msg

        print(colored(f"IntegrationAgent 👩🏿‍💻: {response}", 'red'))
        return response
    
class CheckResponseAgent(Agent):
    def invoke(self, response, query, previous_response, datetime=get_current_utc_datetime(), prompt=check_response_prompt):
      
        planner_prompt = prompt + f"\nresponse: {response} \n\nprevious response: {previous_response} \n\ncurrent datetime: {datetime}"

        messages = [
            {"role": "system", "content": planner_prompt},
            {"role": "user", "content": f"research question: {query}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(colored(f"CheckResponseAgent 👩🏿‍💻: {response}", 'green'))
        return response

class SearchQueryAgent(Agent):
    def invoke(self, query, plan, prompt=generate_searches_prompt):
      
        search_query_prompt = prompt

        messages = [
            {"role": "system", "content": search_query_prompt},
            {"role": "user", "content": f"Query: {query}\n\nPlan: {plan}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(colored(f"SearchQueryAgent 👩🏿‍💻: {response}", 'blue'))
        return response
    

class SearchPageAgent(Agent):
    def invoke(self, response, query, plan, prompt=get_search_page_prompt,search_results=None, failed_sites=None, visited_sites=None):
      
        search_query_prompt = prompt

        messages = [
            {"role": "system", "content": search_query_prompt},
            {"role": "user", "content": f"Query: {query}\n\nPlan: {plan}\n\nSearch Results: {search_results}\n\nFailed Sites: {failed_sites}\n\nVisited Sites: {visited_sites}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(colored(f"SearchPageAgent 👩🏿‍💻: {response}", 'yellow'))
        return response

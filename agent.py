import os 
import yaml
import json
import requests
from termcolor import colored
from scraper.search import scrape_website_content, fetch_search_results
import ast
import google.generativeai as genai
import time
from utils.helper_functions import load_config, get_current_utc_datetime, save_feedback, read_feedback, clear_json_file, initialize_json_file,parse_json
from agents.agents import PlannerAgent,IntegrationAgent,CheckResponseAgent,Agent,SearchQueryAgent,SearchPageAgent


        
if __name__ == '__main__':

    initialize_json_file()
    load_config()
  
    meets_requirements = False
    plan = None
    outputs = None
    integration_agent_response = None
    reason = None
    iterations = 0
    visited_sites = []
    failed_sites = []
    response = None
    feedback = None

    plannerAgent = PlannerAgent(model="gemini-1.5-pro",server="gemini")
    checkResponseAgent = CheckResponseAgent(model="gemini-1.5-pro",server="gemini")
    integrationAgent = IntegrationAgent(model="gemini-1.5-pro",server="gemini")
    searchQueryAgent =  SearchQueryAgent(model="gemini-1.5-pro",server="gemini")
    searchPageAgent = SearchPageAgent(model="gemini-1.5-pro",server="gemini")
    while (query := input("enter you question: ")) != 'exit':   
        while not meets_requirements and iterations < 5:
            iterations += 1
            feedback = read_feedback(json_filename="memory.json")
            
            plan = plannerAgent.invoke(query=query,plan=plan,feedback=feedback)
            search_query_string_json = searchQueryAgent.invoke(query=query,plan=plan)
            search_query = parse_json(search_query_string_json)
            search_results = fetch_search_results(search_query)
            print(colored(f"Search Results: {search_results}", "red"))
            best_page_string_json = searchPageAgent.invoke( plan, query, search_results, failed_sites=[], visited_sites=[])
            best_page = parse_json(best_page_string_json)
            results_dict, failed_sites, response = scrape_website_content(best_page,failed_sites=[])
            attempts = 0

            while not response and attempts < 5:
                print(f"Failed to retrieve content from {best_page}...Trying a different page")
                print(f"Failed Sites: {failed_sites}")
                best_page_string_json = searchPageAgent.invoke(plan, query, search_results, failed_sites, visited_sites=[])
                best_page = parse_json(best_page_string_json)
                results_dict, failed_sites, response = scrape_website_content(best_page,failed_sites=failed_sites)

                attempts += 1
            visited_sites.append(results_dict.get('source', ''))
            integration_agent_response = integrationAgent.invoke(query=query, plan=plan, outputs=results_dict, reason=reason, previous_response=feedback)
            save_feedback(integration_agent_response, json_filename="memory.json")
            
            response_dict = checkResponseAgent.invoke(response=integration_agent_response, query=query, previous_response=feedback)
            response_dict = json.loads(response_dict)

            meets_requirements = response_dict.get('pass', '')
            if meets_requirements == 'True':
                meets_requirements = True
            else: 
                meets_requirements = False
                reason = response_dict.get('reason', '')

        clear_json_file()
        print(colored(f"Final Response: {integration_agent_response}", 'cyan'))

    


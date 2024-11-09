from .security_review_crew.main import SecurityReviewCrew
from rag_management.query_embedding import similarity_search
from .general.main import GeneralCrew
from knowledge_retrieval import util
import os
from dotenv import load_dotenv
load_dotenv()

temp_file = os.getenv('TEMP_FILE')
export_file = os.getenv('EXPORT_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')

class KESCrew:
    def run(self, domain: str, task: str, prompt: str, image_path):
        util.remove_file(temp_file)
        util.remove_file(f"{export_file}.docx")
        util.remove_file(f"{export_file}.pdf")
        util.remove_file(detail_output_file)

        '''
        Task - determine the crew to run
        Domain - determine the RAG data to use (i.e similarity search scope)
        '''
        resp = SecurityReviewCrew().run(system_information=prompt, image_path=image_path)
        return resp

        # if(task == "Security Review" or task == "Threat Modeling"):
        #     rag_context = similarity_search(prompt)
        #     context = f"""
        #         <securityRequirementContextInformation>
        #         {rag_context}
        #         </securityRequirementContextInformation>
        #     """
        #     final_prompt = f"""
        #         <systemInformation>
        #         {prompt}
        #         </systemInformation>
        #     """


    # def run(self, domain: str, task: str, prompt: str, image_path):
    #     util.remove_file(temp_file)
    #     util.remove_file(export_file)
    #     '''
    #     Task - determine the crew to run
    #     Domain - determine the RAG data to use (i.e similarity search scope)
    #     '''

    #     base64_encoded_picture= util.process_file_base64(image_path)

    #     if prompt in ["", None] and base64_encoded_picture in ["", None]:
    #         return
        
    #     if(base64_encoded_picture):
    #         final_prompt = f"Prompt: {prompt}\nImage: {base64_encoded_picture}"
    #     else: 
    #         final_prompt = prompt
    

    #     if(task == "Security Review" or task == "Threat Modeling"):
    #         # Get RAG data based on domain
    #         # Join the data to system information
    #         # Pass the consolidated string as prompt
    #         rag_context = similarity_search(prompt)
    #         context = f"""
    #             <securityRequirementContextInformation>
    #             {rag_context}
    #             </securityRequirementContextInformation>
    #         """
    #         if(base64_encoded_picture):
    #             picture_description = GeneralCrew().run(final_prompt)
    #             new_prompt = picture_description.content
    #         else: 
    #             new_prompt = prompt


    #         final_prompt = f"""
    #             <systemInformation>
    #             {new_prompt}
    #             </systemInformation>
    #         """

    #         resp = SecurityReviewCrew().run(final_prompt, context)
    #         return resp
    #     else:
    #         resp = GeneralCrew().run(final_prompt)
    #         return resp.content

        

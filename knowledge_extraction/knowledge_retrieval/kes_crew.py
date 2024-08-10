from .security_review_crew.main import SecurityReviewCrew
from rag_management.query_embedding import similarity_search
from .general.main import GeneralCrew


class KESCrew:
    def run(self, domain: str, task: str, prompt: str, base64_encoded_picture):
        '''
        Task - determine the crew to run
        Domain - determine the RAG data to use (i.e similarity search scope)
        '''
        if prompt in ["", None] and base64_encoded_picture in ["", None]:
            return
        
        if(base64_encoded_picture):
            final_prompt = f"Prompt: {prompt}\nImage: {base64_encoded_picture}"
        else: 
            final_prompt = prompt
    

        if(task == "Security Review"):
            # Get RAG data based on domain
            # Join the data to system information
            # Pass the consolidated string as prompt
            rag_context = similarity_search(prompt)
            context = f"""
                <securityRequirementContextInformation>
                {rag_context}
                </securityRequirementContextInformation>
            """
            if(base64_encoded_picture):
                picture_description = GeneralCrew().run(final_prompt)
                new_prompt = picture_description.content
            else: 
                new_prompt = prompt


            final_prompt = f"""
                <systemInformation>
                {new_prompt}
                </systemInformation>
            """

            resp = SecurityReviewCrew().run(final_prompt, context)
            return resp
        else:
            resp = GeneralCrew().run(final_prompt)
            return resp.content

        

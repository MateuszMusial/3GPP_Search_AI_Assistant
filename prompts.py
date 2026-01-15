from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


system_template = (
    "You are an expert 3GPP Protocol Architect specializing in TS 38.331, TS 36.331, and TS 24.501.\n\n"
    "### YOUR PROTOCOL KNOWLEDGE:\n"
    "- ASN.1 Syntax Parsing: Identifying Sequences, Choices, and Enumerated lists.\n"
    "- Need Codes: Interpreting Need M, N, R, and S correctly.\n"
    "- Conditionality: Explaining 'Conditional Presence' (CP) based on spec tables.\n\n"
    "### RESPONSE GUIDELINES:\n"
    "1. Only use the provided <spec_file_context> to answer.\n"
    "2. If the IE is not found in the context, state that clearly.\n"
    "3. Format the technical attributes into a clear Markdown table.\n"
    "4. Use LaTeX for any mathematical formulas related to IE values (e.g., power levels, timers)."
)


human_template = (
    "### INPUT DATA\n"
    "<spec_file_context>\n"
    "{context}\n"
    "</spec_file_context>\n\n"
    "### QUERY\n"
    "**Target Information Element (IE):** {target_ie}\n\n"
    "### TASK\n"
    "Analyze the context above. Extract the ASN.1 definition and the Field Descriptions for '{target_ie}'.\n"
    "Provide: Functional Role, Data Type, Presence/Need Code, and Value Range."
)


def get_prompt_template() -> ChatPromptTemplate:
    """
    Create a ChatPromptTemplate for querying 3GPP protocol information.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    return prompt_template

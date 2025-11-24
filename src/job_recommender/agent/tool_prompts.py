from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

system_prompt = """
    You are an expert in Resume Analysis.
"""
resume_summary_prompt = ChatPromptTemplate.from_template("""create a 300 word summery of the resume, Here is the resume content to summarize:
    {resume_content}""")

resume_summary_prompts = ChatPromptTemplate.from_template(
    """
    You are an expert Resume Analyst and Professional Career Writer specializing in creating
    ATS-optimized resume summaries.

    Your task is to generate a concise, high-impact summary based on the provided resume content.

    Follow these steps:

    1. Extract Key Information
    - Core skills and technical competencies
    - Years of experience
    - Industries and domains
    - Quantified achievements and measurable outcomes
    - Tools, technologies, certifications
    - Leadership, project ownership, or cross-functional accomplishments

    2. Create the ATS-Optimized Summary
    - Length: 3–5 sentences (70–120 words)
    - Professional, clear, and keyword-rich
    - Avoid first-person language
    - Focus on accomplishments instead of duties
    - Prioritize clarity, relevance, and scan-ability
    - Use standard job-aligned terminology to maximize ATS parsing accuracy

    3. Output Structure
    Resume Summary:
    [Insert optimized summary]

    Key Strengths (bullet points):
    - [strength 1]
    - [strength 2]
    - [strength 3]

    Here is the resume content to summarize:
    {resume_content}
    """
)

missing_skills_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert ATS (Applicant Tracking System) Analyst and Resume Auditor. 
    Your task is to evaluate the provided resume content and produce a detailed, technical analysis focused on:
    - ATS keyword alignment
    - Skill gaps
    - Missing experience areas
    - Missing tools/technologies
    - Role-specific capability gaps
    - Industry-standard competencies the candidate lacks or does not clearly demonstrate

    INPUT RESUME:
    {resume_content}

    REQUIREMENTS:

    1. ATS Keyword Alignment
    - Identify which crucial ATS keywords (skills, tools, certifications, role-specific terms) are missing.
    - List keywords the candidate has but are weakly represented or not quantifiably supported.
    - Suggest high-value keywords to strengthen ATS matching.

    2. Skill Gaps
    - Provide a structured breakdown of skills the candidate lacks for typical roles in their field.
    - Categorize into:
        - Technical skill gaps  
        - Domain knowledge gaps  
        - Soft skill or leadership gaps  
        - Tool/technology gaps  
        - Experience level gaps  

    3. Missing Areas
    - Identify missing content such as:
        - Metrics or quantified achievements  
        - Industry-specific terminology  
        - Certifications or licenses commonly expected  
        - Project examples, portfolio items, or concrete deliverables  
        - Role clarity (e.g., missing scope, responsibilities, or outcomes)

    4. Output Format
    Return the final answer using this exact structure:

    ATS Keyword Gaps:
    - …

    Skill Gaps:
    - …

    Missing Experience Areas:
    - …

    Missing Tools/Technologies:
    - …

    Recommended Additions (High Impact):
    - …

    Do not provide a resume summary.
    Focus exclusively on gaps, weaknesses, missing elements, and ATS alignment improvements.
    """

)

rode_map_prompt = ChatPromptTemplate.from_template(
    """
    You are a Career Development Strategist and Workforce Planning Specialist. Your task is to create a professional growth roadmap and future-skill plan based on the candidate’s background.

    Input Resume:
    {resume_content}

    Follow this structure to generate a personalized roadmap:

    1. **Career Trajectory Assessment**
    - Identify the candidate’s current level, strengths, specialization, and potential career paths.

    2. **Future Skill Requirements**
    - List high-value skills, tools, certifications, or competencies the candidate should acquire to increase competitiveness and prepare for future industry trends.

    3. **Short-Term Roadmap (0–6 months)**
    - Specific action steps
    - Skills to start learning immediately
    - Courses, certifications, or projects recommended

    4. **Mid-Term Roadmap (6–18 months)**
    - Professional development activities
    - Technical depth/leadership expansion
    - Portfolio or project recommendations

    5. **Long-Term Roadmap (18+ months)**
    - Strategic career advancement goals
    - Roles the candidate could aim for
    - High-level milestone planning

    6. **Output Format**
    Provide the roadmap in these sections:

    **Career Path Assessment:**  
    [text]

    **Short-Term Roadmap (0–6 months):**  
    [bullet list]

    **Mid-Term Roadmap (6–18 months):**  
    [bullet list]

    **Long-Term Roadmap (18+ months):**  
    [bullet list]

    **Recommended Future Skills & Certifications:**  
    [bullet list]
"""

)


extract_keyword_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert Career Data Analyst.  
    Your task is to extract job-related keywords from the content provided.  
    - The input content can be a resume, job description, or any career-related text.  
    - Identify relevant skills, roles, certifications, tools, technologies, and industry-specific terms.  
    - Format the output strictly as a Python list of strings.  
    - No explanations, no extra text, only the list.  

    Input Content: {resume_content}

    Example output:  
    ["keyword01", "keyword02", "keyword03", "keyword04"]
    """
)



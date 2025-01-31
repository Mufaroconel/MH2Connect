import re

def validate_combination(combination: str) -> bool:
    # Check if the combination follows the format "Subject1, Subject2, Subject3"
    pattern = r'^[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+$'
    
    # Match the input against the pattern
    if re.match(pattern, combination.strip()):
        subjects = [subject.strip() for subject in combination.split(',')]
        if len(subjects) == 3:
            return True
    return False


def separate_combination(combination: str):
    # Split the combination by commas and remove extra spaces
    subjects = [subject.strip() for subject in combination.split(',')]
    
    # Ensure that the combination has exactly three subjects
    if len(subjects) == 3:
        Subject1, Subject2, Subject3 = subjects
        return Subject1, Subject2, Subject3
    else:
        return None

def parse_academic_results(results_str):
    """
    Parses a string of subjects and grades in the format:
    'Subject1, A; Subject2, B; Subject3, A; etc.'
    
    Returns a list of tuples where each tuple contains the subject and the grade.
    Example: [("Maths", "A"), ("English", "B"), ("Physics", "C")]
    """
    # Split the input string by semicolon to separate each subject-grade pair
    results = results_str.split(";")
    
    # List to store the parsed subjects and grades
    parsed_results = []
    
    # Iterate through each subject-grade pair
    for result in results:
        # Strip any leading/trailing whitespace and split by comma to separate subject and grade
        subject_grade = result.strip().split(",")
        
        if len(subject_grade) == 2:
            subject = subject_grade[0].strip()
            grade = subject_grade[1].strip()
            parsed_results.append((subject, grade))  # Add the subject and grade to the list
    
    return parsed_results
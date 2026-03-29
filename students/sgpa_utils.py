"""
SGPA (Semester Grade Point Average) Calculation Utility
Converts marks to grade points and calculates semester GPA
"""

from decimal import Decimal


# Grading Scale Conversion
GRADE_SCALE = {
    'A': 4.0,      # 90-100
    'A-': 3.7,     # 85-89
    'B+': 3.3,     # 80-84
    'B': 3.0,      # 75-79
    'B-': 2.7,     # 70-74
    'C+': 2.3,     # 65-69
    'C': 2.0,      # 60-64
    'C-': 1.7,     # 55-59
    'D+': 1.3,     # 50-54
    'D': 1.0,      # 45-49
    'F': 0.0,      # Below 45
}


def marks_to_grade(marks_percentage):
    """
    Convert marks percentage to letter grade
    
    Args:
        marks_percentage (float): Percentage of marks obtained
        
    Returns:
        str: Letter grade (A, A-, B+, etc.)
    """
    marks_percentage = float(marks_percentage)
    
    if marks_percentage >= 90:
        return 'A'
    elif marks_percentage >= 85:
        return 'A-'
    elif marks_percentage >= 80:
        return 'B+'
    elif marks_percentage >= 75:
        return 'B'
    elif marks_percentage >= 70:
        return 'B-'
    elif marks_percentage >= 65:
        return 'C+'
    elif marks_percentage >= 60:
        return 'C'
    elif marks_percentage >= 55:
        return 'C-'
    elif marks_percentage >= 50:
        return 'D+'
    elif marks_percentage >= 45:
        return 'D'
    else:
        return 'F'


def marks_to_grade_point(marks_percentage):
    """
    Convert marks percentage to grade point (0-4 scale)
    
    Args:
        marks_percentage (float): Percentage of marks obtained
        
    Returns:
        float: Grade point (0.0 - 4.0)
    """
    grade = marks_to_grade(marks_percentage)
    return GRADE_SCALE.get(grade, 0.0)


def calculate_course_performance(marks_obtained, total_marks):
    """
    Calculate performance metrics for a single course
    
    Args:
        marks_obtained (Decimal): Marks obtained
        total_marks (Decimal): Total marks
        
    Returns:
        dict: Contains percentage, grade, and grade_point
    """
    marks_obtained = Decimal(str(marks_obtained))
    total_marks = Decimal(str(total_marks))
    
    if total_marks == 0:
        return {
            'percentage': Decimal(0),
            'grade': 'N/A',
            'grade_point': 0.0,
        }
    
    percentage = (marks_obtained / total_marks) * 100
    grade_point = marks_to_grade_point(float(percentage))
    grade = marks_to_grade(float(percentage))
    
    return {
        'percentage': round(percentage, 2),
        'grade': grade,
        'grade_point': grade_point,
    }


def calculate_sgpa(grades_list, credits_list=None):
    """
    Calculate Semester GPA from a list of grades
    
    Args:
        grades_list (list): List of Grade objects or performance dicts
        credits_list (list, optional): List of credit hours for each course
                                      Defaults to 3 credits per course
        
    Returns:
        dict: Contains SGPA, total_credits, grade_count, etc.
    """
    if not grades_list:
        return {
            'sgpa': 0.0,
            'total_credits': 0,
            'grade_count': 0,
            'weighted_sum': 0.0,
        }
    
    # Default credits per course if not provided
    if credits_list is None:
        credits_list = [3] * len(grades_list)
    
    total_credit_hours = Decimal(0)
    weighted_sum = Decimal(0)
    grade_count = 0
    
    for i, grade_data in enumerate(grades_list):
        credit = Decimal(str(credits_list[i]))
        
        # Handle Grade objects
        if hasattr(grade_data, 'marks_obtained'):
            performance = calculate_course_performance(
                grade_data.marks_obtained,
                grade_data.total_marks
            )
            grade_point = Decimal(str(performance['grade_point']))
        else:
            # Handle dict performance data
            grade_point = Decimal(str(grade_data.get('grade_point', 0)))
        
        total_credit_hours += credit
        weighted_sum += (grade_point * credit)
        grade_count += 1
    
    # Calculate SGPA
    if total_credit_hours > 0:
        sgpa = round(float(weighted_sum / total_credit_hours), 2)
    else:
        sgpa = 0.0
    
    return {
        'sgpa': sgpa,
        'total_credits': int(total_credit_hours),
        'grade_count': grade_count,
        'weighted_sum': float(weighted_sum),
        'interpretation': get_sgpa_interpretation(sgpa),
    }


def get_sgpa_interpretation(sgpa):
    """
    Get text interpretation of SGPA score
    
    Args:
        sgpa (float): SGPA value
        
    Returns:
        dict: Contains rating and description
    """
    sgpa = float(sgpa)
    
    if sgpa >= 3.5:
        return {
            'rating': 'Excellent',
            'description': 'Outstanding performance',
            'color': 'green',
        }
    elif sgpa >= 3.0:
        return {
            'rating': 'Good',
            'description': 'Very good performance',
            'color': 'blue',
        }
    elif sgpa >= 2.5:
        return {
            'rating': 'Satisfactory',
            'description': 'Satisfactory performance',
            'color': 'yellow',
        }
    elif sgpa >= 2.0:
        return {
            'rating': 'Average',
            'description': 'Average performance',
            'color': 'orange',
        }
    else:
        return {
            'rating': 'Below Average',
            'description': 'Needs improvement',
            'color': 'red',
        }


def calculate_cumulative_gpa(all_grades_list, credits_list=None):
    """
    Calculate Cumulative GPA across multiple semesters/courses
    
    Args:
        all_grades_list (list): All grades from all courses/semesters
        credits_list (list, optional): Credits for each course
        
    Returns:
        dict: Contains CGPA and overall statistics
    """
    return calculate_sgpa(all_grades_list, credits_list)

"""Test data for team estimation flow"""

TEST_ESTIMATES = {
    'backend_dev': {
        'estimates': {
            'story_points': {'value': 8, 'confidence': 'HIGH'},
            'person_days': {'value': 5, 'confidence': 'MEDIUM'}
        },
        'justification': [
            {
                'title': 'Technical Complexity',
                'content': 'Backend implementation requires careful handling of parallel processing...'
            },
            {
                'title': 'Integration Points',
                'content': 'Need to coordinate with multiple Lambda functions and DynamoDB...'
            }
        ]
    },
    'frontend_dev': {
        'estimates': {
            'story_points': {'value': 5, 'confidence': 'MEDIUM'},
            'person_days': {'value': 3, 'confidence': 'HIGH'}
        },
        'justification': [
            {
                'title': 'UI Components',
                'content': 'Need to implement circular visualization and modal dialogs...'
            }
        ]
    },
    'devops_engineer': {
        'estimates': {
            'story_points': {'value': 3, 'confidence': 'HIGH'},
            'person_days': {'value': 2, 'confidence': 'HIGH'}
        },
        'justification': [
            {
                'title': 'Infrastructure Impact',
                'content': 'Lambda configurations and DynamoDB capacity planning...'
            }
        ]
    }
}

def get_test_estimate(role: str) -> dict:
    """Returns test estimate data for a specific role"""
    return TEST_ESTIMATES.get(role, {}) 
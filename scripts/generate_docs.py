import os
import re
import ast
from pathlib import Path

class DocGenerator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.lambda_template = self._read_template('docs/templates/lambda_template.md')
        
    def _read_template(self, path):
        with open(self.project_root / path, 'r') as f:
            return f.read()
            
    def parse_lambda_file(self, file_path):
        """Extract documentation from Lambda function file"""
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Parse Python file
        tree = ast.parse(content)
        
        # Extract docstring
        docstring = ast.get_docstring(tree)
        
        # Extract environment variables
        env_vars = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Name) and node.value.id == 'os.environ':
                    if isinstance(node.slice, ast.Constant):
                        env_vars.append(node.slice.value)
        
        # Extract function info
        function_info = {
            'name': Path(file_path).stem,
            'path': str(file_path.relative_to(self.project_root)),
            'docstring': docstring,
            'env_vars': env_vars
        }
        
        return function_info
        
    def generate_lambda_doc(self, lambda_path):
        """Generate documentation for a Lambda function"""
        info = self.parse_lambda_file(lambda_path)
        
        # Find corresponding test file
        test_file = self.project_root / 'backend/tests' / f'test_{info["name"]}.py'
        test_path = str(test_file.relative_to(self.project_root)) if test_file.exists() else "Not found"
        
        # Generate documentation
        doc = self.lambda_template.replace('[Name]', info['name'])
        doc = doc.replace('`backend/src/[function_name]/app.py`', f'`{info["path"]}`')
        
        # Add docstring content
        if info['docstring']:
            doc = self._insert_docstring_content(doc, info['docstring'])
            
        # Add environment variables
        env_vars_text = '\n'.join([f'- `{var}`: Description needed' for var in info['env_vars']])
        doc = doc.replace('- `VAR_NAME`: Description', env_vars_text)
        
        return doc
        
    def generate_all_docs(self):
        """Generate documentation for all Lambda functions"""
        lambda_dir = self.project_root / 'backend/src'
        
        for lambda_path in lambda_dir.glob('*/app.py'):
            doc = self.generate_lambda_doc(lambda_path)
            
            # Write to docs directory
            doc_path = self.project_root / 'docs/lambdas' / f'{lambda_path.parent.name}.md'
            doc_path.parent.mkdir(exist_ok=True)
            
            with open(doc_path, 'w') as f:
                f.write(doc)
                
if __name__ == '__main__':
    generator = DocGenerator()
    generator.generate_all_docs() 
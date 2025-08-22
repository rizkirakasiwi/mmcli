# Contributor Guidance

Thank you for your interest in contributing to MMCLI! This document provides guidelines and requirements for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Git
- Basic familiarity with command-line tools

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/mmcli.git
   cd mmcli
   ```
3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
4. **Install development dependencies**:
   ```bash
   pip install -e .[test]
   ```

## ✅ Testing Requirements

**⚠️ CRITICAL: All tests must pass before submitting a Pull Request**

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test files
pytest tests/test_command_manager.py   # CLI parsing tests
pytest tests/test_media_converter.py   # Conversion functionality
pytest tests/test_media_downloader.py  # Download functionality
pytest tests/test_media_format.py      # Format validation
pytest tests/test_integration.py       # End-to-end tests

# Run with verbose output
pytest -v
```

### Test Coverage

Our test suite includes:
- **Unit tests** - Individual function testing
- **Integration tests** - Full CLI command workflows
- **Mock-based tests** - Avoid external dependencies during testing
- **Error handling** - Validation of error scenarios
- **CLI validation** - Argument parsing and help messages

### Viewing Coverage Reports

After running tests with coverage:
```bash
# View HTML coverage report
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html # Windows
```

## 🔧 Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow existing code style and conventions
- Add tests for new functionality
- Update documentation if needed

### 3. Test Your Changes
```bash
# Run full test suite
pytest --cov=app --cov-report=term-missing

# Ensure all tests pass
echo $?  # Should output 0 (success)
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

**Commit Message Guidelines:**
- `feat:` - New features
- `fix:` - Bug fixes
- `test:` - Adding or updating tests
- `docs:` - Documentation changes
- `refactor:` - Code refactoring

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] **All tests pass locally** (`pytest`)
- [ ] **Code coverage is maintained** (aim for >80%)
- [ ] **New functionality has tests**
- [ ] **Documentation is updated** (if applicable)
- [ ] **Commit messages are clear**
- [ ] **No breaking changes** (or clearly documented)

## 🧪 Writing Tests

### Test Structure
```
tests/
├── test_command_manager.py    # CLI argument parsing and --version
├── test_media_converter.py    # File conversion logic  
├── test_media_downloader.py   # Download functionality
├── test_media_format.py       # Format mappings and validation
└── test_integration.py        # End-to-end workflows
```

### Test Guidelines

1. **Mock external dependencies** (ffmpeg, YouTube, file system)
2. **Test both success and error scenarios**
3. **Use descriptive test names**:
   ```python
   def test_convert_single_file_success(self):
   def test_convert_single_file_invalid_format(self):
   ```

4. **Create temporary test files when needed**
5. **Clean up test artifacts**

### Example Test Pattern
```python
import pytest
from unittest.mock import patch, MagicMock

class TestYourFeature:
    def setup_method(self):
        """Set up test fixtures"""
        pass
        
    def teardown_method(self):
        """Clean up after tests"""
        pass
        
    @patch('your.module.dependency')
    def test_your_function_success(self, mock_dependency):
        """Test successful execution"""
        # Arrange
        mock_dependency.return_value = "expected_result"
        
        # Act
        result = your_function()
        
        # Assert
        assert result == "expected_result"
        mock_dependency.assert_called_once()
```

## 🏗️ Code Style Guidelines

### General Principles
- **Follow PEP 8** for Python code style
- **Use meaningful variable names**
- **Keep functions small and focused**
- **Add docstrings for public functions**

### Example Code Style
```python
def convert_single_file(input_file: Path, output_format: str, output_dir: Path) -> bool:
    """Convert a single file to specified format.
    
    Args:
        input_file: Path to input file
        output_format: Target format (e.g., 'mp3', 'jpg')
        output_dir: Directory for output file
        
    Returns:
        True if conversion successful, False otherwise
    """
```

## 🐛 Debugging Tests

### Common Issues

1. **Import errors**: Ensure you're running from project root
2. **Missing dependencies**: Run `pip install -e .[test]`
3. **Path issues**: Use absolute paths in tests
4. **Mock not working**: Check mock target path is correct

### Debugging Commands
```bash
# Run single test with debug output
pytest tests/test_your_file.py::test_function_name -v -s

# Run tests without capturing output
pytest --capture=no

# Drop into debugger on failure
pytest --pdb
```

## 🚫 What NOT to Contribute

Please avoid:
- **Malicious code** or security vulnerabilities
- **Breaking changes** without discussion
- **Code without tests**
- **Large refactoring** without prior discussion
- **Dependencies without justification**

## 📞 Getting Help

- **Create an issue** for bugs or feature requests
- **Start a discussion** for architectural questions
- **Ask in PR comments** for code-specific questions

## 📚 Project Structure

```
mmcli/
├── app/
│   ├── tools/
│   │   ├── media_converter.py    # File conversion logic
│   │   └── media_downloader.py   # YouTube download functionality
│   └── utils/
│       ├── command_manager.py    # CLI argument parsing
│       └── media_format.py       # Format definitions and mappings
├── bin/
│   ├── mmcli                     # Main CLI entry point
│   └── install.*                 # Installation scripts
├── tests/                        # Comprehensive test suite
│   ├── test_command_manager.py   # CLI parsing tests
│   ├── test_media_converter.py   # Conversion functionality
│   ├── test_media_downloader.py  # Download functionality
│   ├── test_media_format.py      # Format validation
│   └── test_integration.py       # End-to-end tests
├── main.py                       # Application entry point
└── pyproject.toml                # Package configuration
```

## 🎯 Types of Contributions Needed

- **Bug fixes** - Fix existing issues
- **New formats** - Add support for more media formats
- **Performance** - Optimize conversion/download speed
- **Error handling** - Better user error messages
- **Documentation** - Improve guides and examples
- **Tests** - Increase coverage and test scenarios

---

Happy coding! 🎉
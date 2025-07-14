# GitHub Actions Workflow Configuration

This directory contains automated workflows for the DSA Media Player project.

## Available Workflows

### 1. `ci.yml` - Main CI/CD Pipeline
**Triggers:** Push to main/integration-prep, Pull requests to main
**Features:**
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
- Code quality checks (Black, isort, flake8)
- Individual data structure testing
- Unit tests with coverage reporting
- Integration testing
- Security scanning with Safety and Bandit
- Performance testing
- Branch validation

### 2. `feature-branch.yml` - Feature Branch Testing
**Triggers:** Push to feature branches (regNo_*, feature/*, bugfix/*)
**Features:**
- Branch-specific testing based on naming convention
- Code structure validation
- Compatibility testing with main branch
- Merge simulation

### 3. `pr-validation.yml` - Pull Request Validation
**Triggers:** Pull request creation/updates
**Features:**
- PR title and description validation
- Changed files analysis
- Targeted testing based on modifications
- Code quality assessment
- Merge conflict detection
- Documentation checks

### 4. `release.yml` - Release and Deployment
**Triggers:** Release creation, Manual dispatch
**Features:**
- Release artifact creation
- Cross-platform installation scripts
- Package building and testing
- Documentation generation
- Release validation

## Workflow Status Badges

Add these badges to your README.md:

```markdown
![CI/CD](https://github.com/ClaudeKa/dsa-sem-project-cousins_dsa/workflows/DSA%20Media%20Player%20CI%2FCD/badge.svg)
![Feature Branch Tests](https://github.com/ClaudeKa/dsa-sem-project-cousins_dsa/workflows/Feature%20Branch%20Tests/badge.svg)
![PR Validation](https://github.com/ClaudeKa/dsa-sem-project-cousins_dsa/workflows/Pull%20Request%20Validation/badge.svg)
```

## Workflow Configuration

### Automated Testing Matrix
- **Python Versions:** 3.8, 3.9, 3.10, 3.11
- **Operating System:** Ubuntu Latest
- **Test Coverage:** Unit tests, Integration tests, Performance tests
- **Code Quality:** Formatting, Linting, Import sorting

### Branch Protection Rules (Recommended)
```yaml
Protection Rules for main branch:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Required status checks:
  - Test Suite (Python 3.10)
  - Integration Tests
  - PR Validation
- Require pull request reviews before merging
- Dismiss stale PR approvals when new commits are pushed
```

### Environment Variables
No special environment variables required. All workflows use standard GitHub Actions environment.

## Usage Examples

### Running Workflows Manually
1. Go to Actions tab in GitHub repository
2. Select "Release and Deploy" workflow
3. Click "Run workflow"
4. Enter version number (e.g., v1.0.0)
5. Click "Run workflow"

### Triggering Feature Branch Testing
```bash
# Create and push feature branch
git checkout -b regNo_123456_new_feature
git push origin regNo_123456_new_feature
# Workflow automatically triggers
```

### Creating a Release
1. Go to Releases section in GitHub
2. Click "Create a new release"
3. Tag version: v1.0.0
4. Release title: "DSA Media Player v1.0.0"
5. Describe changes
6. Click "Publish release"
7. Release workflow automatically creates artifacts

## Troubleshooting

### Common Issues

1. **Import Errors in Workflows**
   - Ensure all `__init__.py` files are present
   - Check Python path setup in workflow

2. **Test Failures**
   - Check if all dependencies are installed
   - Verify database initialization

3. **Code Quality Issues**
   - Run `black`, `isort`, `flake8` locally before pushing
   - Fix formatting and linting issues

### Debugging Workflows
1. Check workflow logs in Actions tab
2. Look for specific error messages
3. Test locally with same Python version
4. Ensure all required files are committed

## Best Practices

### For Contributors
1. **Before Creating PR:**
   ```bash
   # Run local tests
   python -m pytest tests/
   
   # Check code quality
   black --check src/ tests/
   isort --check-only src/ tests/
   flake8 src/ tests/
   ```

2. **Branch Naming:**
   - Use convention: `regNo_XXXXXX_feature_name`
   - Example: `regNo_123456_queue_implementation`

3. **Commit Messages:**
   - Use conventional commits: `feat: add queue implementation`
   - Be descriptive about changes

### For Maintainers
1. **Reviewing PRs:**
   - Wait for all checks to pass
   - Review code quality reports
   - Test functionality manually if needed

2. **Creating Releases:**
   - Use semantic versioning (v1.0.0)
   - Include comprehensive release notes
   - Test release artifacts before publishing

## Monitoring and Maintenance

### Workflow Health
- Monitor workflow success rates
- Update Python versions annually
- Review and update dependencies regularly
- Check for security vulnerabilities

### Performance Optimization
- Cache dependencies when possible
- Parallelize independent jobs
- Optimize test execution time
- Use matrix strategies effectively

## Contributing to Workflows

1. Test changes in feature branch first
2. Update documentation when modifying workflows
3. Consider impact on all team members
4. Follow GitHub Actions best practices

For more information about GitHub Actions, see the [official documentation](https://docs.github.com/en/actions).

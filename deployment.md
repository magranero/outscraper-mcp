# Deployment Guide

This guide covers how to deploy the Outscraper MCP server for both local use and via Smithery.

## 🚀 Quick Start

### For Users

**Via Smithery (Recommended):**
```bash
npx -y @smithery/cli install outscraper-mcp --client claude
```

**Via PyPI:**
```bash
pip install outscraper-mcp
# or
uvx outscraper-mcp
```

## 🔧 For Developers

### Local Development

1. **Clone and Setup:**
   ```bash
   git clone https://github.com/jayozer/outscraper-mcp
   cd outscraper-mcp
   uv sync
   ```

2. **Set Environment:**
   ```bash
   cp env.sample .env
   # Edit .env with your OUTSCRAPER_API_KEY
   ```

3. **Test Installation:**
   ```bash
   ./scripts/test-install.sh
   ```

### Publishing to PyPI

1. **Build Package:**
   ```bash
   ./scripts/build.sh
   ```

2. **Test on TestPyPI:**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

3. **Publish to PyPI:**
   ```bash
   python -m twine upload dist/*
   ```

### Publishing to Smithery

1. **Ensure the repository is properly configured:**
   - `smithery.yaml` is configured for container deployment
   - `Dockerfile` is present and functional
   - HTTP server module is working (`server_http.py`)

2. **Submit to Smithery:**
   - Create account at [smithery.ai](https://smithery.ai)
   - Connect your GitHub repository
   - Navigate to Deployments tab
   - Click Deploy to build and host your container

3. **Configuration Requirements:**
   - Repository must have `smithery.yaml` with `runtime: "container"`
   - Dockerfile must expose HTTP endpoint at `/mcp`
   - Server must listen on `PORT` environment variable
   - Container must handle configuration via query parameters

4. **Update Documentation:**
   - Add Smithery badge to README
   - Update installation instructions

## 📋 Deployment Checklist

### Pre-deployment
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version is bumped in `pyproject.toml`
- [ ] Changelog is updated
- [ ] License is current

### PyPI Deployment
- [ ] Package builds successfully
- [ ] Package passes `twine check`
- [ ] TestPyPI deployment works
- [ ] Production PyPI deployment
- [ ] Installation verification

### Smithery Deployment
- [ ] PyPI package is available
- [ ] `smithery.yaml` is configured
- [ ] Smithery submission completed
- [ ] Badge is added to README
- [ ] Installation via Smithery works

### Post-deployment
- [ ] Update GitHub release
- [ ] Test installation methods
- [ ] Update documentation
- [ ] Announce on relevant channels

## 🔄 Continuous Integration

The repository includes GitHub Actions for automated:
- Building and testing
- Publishing to PyPI on version tags
- Creating GitHub releases
- Package verification

### Setting up GitHub Actions

1. **Enable trusted publishing on PyPI:**
   - Go to PyPI project settings
   - Add GitHub Actions as trusted publisher
   - Configure environment names: `pypi` and `testpypi`

2. **Create version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Monitor deployment:**
   - Check GitHub Actions workflow
   - Verify PyPI package
   - Test installation

## 🐛 Troubleshooting

### Common Issues

**Build Failures:**
- Check Python version compatibility
- Verify all dependencies are specified
- Ensure `pyproject.toml` is valid

**PyPI Upload Issues:**
- Verify trusted publishing is configured
- Check package name availability
- Ensure version number is incremented

**Smithery Issues:**
- Verify `smithery.yaml` uses `runtime: "container"` format
- Check that Dockerfile is present and builds successfully
- Ensure HTTP server exposes `/mcp` endpoint correctly
- Verify server listens on `PORT` environment variable
- Test container locally before deploying:
  ```bash
  docker build -t outscraper-mcp .
  docker run -p 8000:8000 -e PORT=8000 outscraper-mcp
  curl http://localhost:8000/health
  curl http://localhost:8000/mcp
  ```
- Check deployment logs in Smithery dashboard
- Ensure all dependencies are properly specified in pyproject.toml

### Testing Locally

```bash
# Test package installation
pip install dist/outscraper_mcp-*.whl

# Test CLI
outscraper-mcp --help

# Test import
python -c "import outscraper_mcp; print(outscraper_mcp.__version__)"
```

## 📚 Additional Resources

- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Smithery Documentation](https://smithery.ai/docs)
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [Model Context Protocol](https://modelcontextprotocol.io/) 
from setuptools import setup, find_packages

setup(
    name="kube-ai-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Sumit Purandare",
    description="AI-powered Kubernetes log analyzer",
    python_requires=">=3.8",
    entry_points={
    "console_scripts": [
        "kube-ai=kube_ai_analyzer.cli:main",
    ],
  },
)


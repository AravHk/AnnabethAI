@echo off
echo 🚀 Starting Agentic Travel Planner...
echo 📱 Opening web interface...

streamlit run src/presentation/app.py --server.port 8501 --server.address localhost

pause
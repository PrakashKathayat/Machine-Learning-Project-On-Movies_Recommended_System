mkdir -p ~/.streamlit/credentials.toml

echo "\
[server]\n\
port = $PORRT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"flaben10@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = $PORT\n\
maxUploadSize = 500\n\
maxMessageSize = 500\n\
" > ~/.streamlit/config.toml

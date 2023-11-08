# Chat with Git Repository: A Streamlit Application

This application is a Streamlit-based web application that allows users to upload a zipped GitHub repository and ask questions about it. The application uses the Llama library to create a conversational AI that can answer questions about the contents of the repository.

## Features

- Upload a zipped GitHub repository.
- Ask questions about the uploaded repository.
- Get AI-generated responses to your questions.

## Installation

To run this application, you'll need to install the required Python libraries. You can do this by running the following command:

```bash
pip install streamlit llama
```

You'll also need to set up the OpenAI API key in your environment. You can do this by setting the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

## Usage

To start the application, navigate to the directory containing the application and run the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the application in your web browser.

Once the application is running, you can use it as follows:

1. In the sidebar, enter your password in the "Authentication" section. The default password is set in the `.env` file.

2. In the "Your Repository" section, click "Browse files" to upload your zipped GitHub repository.

3. After uploading the repository, click "Process" to process the repository. This will unzip the repository, read the contents of the files, and create an AI chat engine that can answer questions about the repository.

4. In the main section of the application, enter your question in the "Ask a question about your repository:" field and press Enter. The application will display an AI-generated response to your question.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
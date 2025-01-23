FROM python:3.12.6

ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=$GEMINI_API_KEY

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
ENV PORT=8000
ENV HOST=0.0.0.0

CMD ["python", "main.py"]

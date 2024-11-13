FROM python:3.12

RUN useradd -m -u 1000 server
USER server
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=server ./backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=server ./backend /app
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:7860"]

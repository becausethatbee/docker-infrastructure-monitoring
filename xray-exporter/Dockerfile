FROM python:3.11-alpine

COPY exporter.py /exporter.py
RUN chmod +x /exporter.py

EXPOSE 9550

CMD ["/usr/local/bin/python3", "/exporter.py"]

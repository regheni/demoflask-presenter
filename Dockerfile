FROM python
RUN mkdir -p /app/
WORKDIR /app
RUN apt update && apt install zsh -y
RUN chsh -s /usr/bin/zsh
RUN sh -c sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
SHELL ["/bin/zsh", "-c"]

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN pip install -e .
ENV FLASK_APP=app
ENV FLASK ENV=development
EXPOSE 5001:3000
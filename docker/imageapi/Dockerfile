FROM python:3.7

MAINTAINER Alex Tarasenko <alextar.21@gmail.com>


RUN apt-get update && apt-get install -y openssh-server
RUN apt-get install nano
RUN apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*
RUN mkdir /var/run/sshd
RUN echo root:root | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin/PermitRootLogin/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
EXPOSE 51234


# Custom Supervisord config
COPY docker/imageapi/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#COPY docker/frontend_api/setup_cython.py /usr/local/lib/python3.6/site-packages/setup_cython.py
RUN mkdir -p /service/www/imageapi
COPY ./imageapi /service/www/imageapi
COPY ./imageapi/requirements.txt /service/www/imageapi/requirements.txt
WORKDIR /service/www/imageapi
RUN pip install --upgrade pip
RUN pip install -r /service/www/imageapi/requirements.txt
#RUN npm install
#RUN python "/usr/local/lib/python3.5/site-packages/setup_cython.py" build_ext --inplace
#ENTRYPOINT ["python"]
#CMD ["main.py"]
#CMD ["/usr/sbin/sshd", "-D"]
CMD ["/usr/bin/supervisord"]
#CMD ["gunicorn -c gunicorn.py imageapi.wsgi"]


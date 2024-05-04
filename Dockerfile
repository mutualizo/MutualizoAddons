FROM mutualizo_base_14:latest

WORKDIR /opt/sources/

RUN touch /var/log/odoo/odoo-server.log && \
    touch /var/run/odoo.pid

COPY ./odoo.conf /opt/
COPY ./entrypoint.sh /
COPY ./wait-for-psql.py /usr/local/bin/wait-for-psql.py

RUN mkdir -p /opt/addons/MutualizoAddons

COPY ./apps/ /opt/addons/MutualizoAddons/

RUN chown -R odoo:odoo /opt/addons && \
    chown -R odoo:odoo /opt/data && \
    chown -R odoo:odoo /var/log/odoo && \
    chown -R odoo:odoo /etc/odoo && \
    chown odoo:odoo /var/run/odoo.pid

RUN ln -s /opt/odoo/odoo-bin /usr/bin/odoo-server

# Clear instalation
RUN rm -R /opt/sources/*
RUN apt-get autoremove -y && \
    apt-get autoclean

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

WORKDIR /opt/

USER root

VOLUME ["/opt/data"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

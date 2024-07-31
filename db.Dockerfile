FROM ankane/pgvector

# Copy custom entrypoint script
COPY custom-entrypoint.sh /docker-entrypoint-initdb.d/

# Ensure the custom entrypoint script is executable
RUN chmod +x /docker-entrypoint-initdb.d/custom-entrypoint.sh

EXPOSE 5432

ENTRYPOINT ["/docker-entrypoint-initdb.d/custom-entrypoint.sh"]



# ARG PG_MAJOR=16
# FROM postgres:$PG_MAJOR
# ARG PG_MAJOR

# COPY . /tmp/pgvector

# RUN apt-get update && \
# 		apt-mark hold locales && \
# 		apt-get install -y --no-install-recommends build-essential make ostgresql-server-dev-$PG_MAJOR && \
# 		cd /tmp/pgvector && \
# 		make clean && \
# 		make OPTFLAGS="" && \
# 		make install && \
# 		mkdir /usr/share/doc/pgvector && \
# 		cp LICENSE README.md /usr/share/doc/pgvector && \
# 		rm -r /tmp/pgvector && \
# 		apt-get remove -y build-essential postgresql-server-dev-$PG_MAJOR && \
# 		apt-get autoremove -y && \
# 		apt-mark unhold locales && \
# 		rm -rf /var/lib/apt/lists/*


# FROM postgres:latest

# RUN apt-get update && \
#     apt-get install -y build-essential wget && \
#     wget https://github.com/pgvector/pgvector/archive/refs/tags/v0.2.0.tar.gz && \
#     tar -xzf v0.2.0.tar.gz && \
#     cd pgvector-0.2.0 && \
#     make && \
#     make install && \
#     cd .. && \
#     rm -rf pgvector-0.2.0 v0.2.0.tar.gz && \
#     apt-get remove -y build-essential wget && \
#     apt-get autoremove -y && \
#     apt-get clean

# # Install required packages
# RUN apt-get update && \
#     apt-get install -y git build-essential postgresql-server-dev-16 && \
#     git clone https://github.com/pgvector/pgvector.git && \
#     cd pgvector && \
#     make && \
#     make install && \
#     cd .. && \
#     rm -rf pgvector && \
#     apt-get remove -y git build-essential && \
#     apt-get autoremove -y && \
#     apt-get clean



ARG NUXEO_VERSION=2025

FROM docker-private.packages.nuxeo.com/nuxeo/nuxeo:${NUXEO_VERSION}

ARG BUILD_TAG=unknown
ARG SCM_REF=unknown
ARG VERSION=unknown

LABEL com.hyland.mcp-demo.build-tag=$BUILD_TAG
LABEL com.hyland.mcp-demo.scm-ref=$SCM_REF
LABEL com.hyland.mcp-demo.version=$VERSION

USER root
# install RPM Fusion free repository
RUN dnf -y install --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm \
    && dnf -y --enablerepo=ol9_codeready_builder install ffmpeg \
    && dnf clean all
USER 900

# Install remote packages
RUN --mount=type=secret,id=CLID,env=CLID /install-packages.sh --clid ${CLID} \
    nuxeo-audit-opensearch1 \
    nuxeo-opensearch1-embed \
    nuxeo-search-client-opensearch1 \
    nuxeo-showcase-content \
    nuxeo-web-ui

# COPY --chmod only supports octal notation, using 775 that is equivalent to rwxrwxr-x
COPY --chown=900:0 --chmod=775 rootfs /

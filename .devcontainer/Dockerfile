FROM manimcommunity/manim:stable

USER root

# Fonts — fără ele, Pango produce SVG gol și Manim crapă la primul Text()
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        fontconfig \
        fonts-dejavu \
        fonts-liberation2 \
        fonts-noto-core \
        xdg-utils \
        vlc && \
    fc-cache -fv && \
    rm -rf /var/lib/apt/lists/*

USER manimuser
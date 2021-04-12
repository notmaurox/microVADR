FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

# The following adapted from https://github.com/andersgs/docker-builds/blob/master/vadr/1.1.2/Dockerfile
ENV VADR_VERSION="1.1.3"\
  VADR_CORONA_MODELS_VERSION="1.2-1" \
  LC_ALL=C \
  VADRINSTALLDIR=/opt/vadr

ENV VADRSCRIPTSDIR=$VADRINSTALLDIR/vadr \
 VADRMODELDIR=$VADRINSTALLDIR/vadr-models \
 VADRINFERNALDIR=$VADRINSTALLDIR/infernal/binaries \
 VADREASELDIR=$VADRINSTALLDIR/infernal/binaries \
 VADRHMMERDIR=$VADRINSTALLDIR/hmmer/binaries \
 VADRBIOEASELDIR=$VADRINSTALLDIR/Bio-Easel \
 VADRSEQUIPDIR=$VADRINSTALLDIR/sequip \
 VADRBLASTDIR=$VADRINSTALLDIR/ncbi-blast/bin

ENV PERL5LIB=$VADRSCRIPTSDIR:$VADRSEQUIPDIR:$VADRBIOEASELDIR/blib/lib:$VADRBIOEASELDIR/blib/arch:$PERL5LIB \
 PATH=$VADRSCRIPTSDIR:$PATH

# install dependencies via apt-get. Clean up apt garbage 
RUN apt-get update && apt-get install -y \
 wget \
 perl \
 curl \
 unzip \
 build-essential \
 autoconf && \
 apt-get install -y libinline-c-perl liblwp-protocol-https-perl && \
 apt-get autoclean && rm -rf /var/lib/apt/lists/*

# install and/or setup more things. Make /data for use as a working dir
RUN mkdir -p ${VADRINSTALLDIR} && \
 cd ${VADRINSTALLDIR} &&\
 # wget https://raw.githubusercontent.com/ncbi/vadr/release-${VADR_VERSION}/vadr-install.sh -T 250 &&\
 bash /app/vadr-install.sh linux

# install the latest corona virus models
RUN wget -O vadr-models-corona.tar.gz https://ftp.ncbi.nlm.nih.gov/pub/nawrocki/vadr-models/coronaviridae/${VADR_CORONA_MODELS_VERSION}/vadr-models-corona-${VADR_CORONA_MODELS_VERSION}.tar.gz -T 250
RUN mkdir -p ${VADRMODELDIR}
RUN tar -xf vadr-models-corona.tar.gz -C ${VADRMODELDIR}
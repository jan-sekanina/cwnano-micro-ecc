TARGET = micro-ecc

SRC += main.c uECC.c

PLATFORM = CWNANO

ifeq ($(PLATFORM),CW308_XMEGA)

else ifeq ($(PLATFORM),CWNANO)

else ifeq ($(PLATFORM),CW308_STM32F0)

else ifeq ($(PLATFORM),CW308_STM32F3)

else ifeq ($(PLATFORM),HOST)

else
  $(error Invalid or empty PLATFORM: $(PLATFORM))
endif

include simpleserial/Makefile.simpleserial

FIRMWAREPATH = .
include Makefile.inc

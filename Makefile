TARGET = micro-ecc

SRC += main.c uecc/uECC.c

MKDIR_LIST += uecc

EXTRAINCDIRS += uecc

CDEFS += -DuECC_SUPPORTS_secp160r1=0 -DuECC_SUPPORTS_secp192r1=0 -DuECC_SUPPORTS_secp224r1=0 -DuECC_SUPPORTS_secp256k1=0 -DuECC_SUPPORT_COMPRESSED_POINT=0 -DuECC_OPTIMIZATION_LEVEL=2

PLATFORM ?= CWNANO

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

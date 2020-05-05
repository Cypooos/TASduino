MCU          = atmega16u2
ARCH         = AVR8
F_CPU        = 16000000
F_USB        = $(F_CPU)
OPTIMIZATION = s
INCLUDE_DIR  = core/compiler/include
TARGET       = spam-a
SRC_DIR      = core/compiler/src
SRC          = $(SRC_DIR)/Joystick.c $(SRC_DIR)/Descriptors.c $(SRC_DIR)/bot/$(TARGET).c $(LUFA_SRC_USB)
LUFA_PATH    = ../LUFA
CC_FLAGS     = -DUSE_LUFA_CONFIG_HEADER -Iinclude/
LD_FLAGS     =

# Default target
all:

# Include LUFA build script makefiles
include $(LUFA_PATH)/Build/lufa_core.mk
include $(LUFA_PATH)/Build/lufa_sources.mk
include $(LUFA_PATH)/Build/lufa_build.mk
include $(LUFA_PATH)/Build/lufa_cppcheck.mk
include $(LUFA_PATH)/Build/lufa_doxygen.mk
include $(LUFA_PATH)/Build/lufa_dfu.mk
include $(LUFA_PATH)/Build/lufa_hid.mk
include $(LUFA_PATH)/Build/lufa_avrdude.mk
include $(LUFA_PATH)/Build/lufa_atprogram.mk

# Target for LED/buzzer to alert when print is done
with-alert: all
with-alert: CC_FLAGS += -DALERT_WHEN_DONE

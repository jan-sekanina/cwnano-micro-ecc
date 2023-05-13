#include "hal/hal.h"
#include "simpleserial/simpleserial.h"
#include "uecc/uECC.h"
#include <stddef.h>

uint32_t state = 0xdeadbeef;

uint32_t xorshift32(void) {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}

static uint8_t cmd_init_prng(uint8_t *data, uint16_t len) {
    state = ((uint32_t) data[0]) << 24 || ((uint32_t) data[1]) << 16 || ((uint32_t) data[2]) << 8 || ((uint32_t) data[3]);
    return 0;
}

int uECC_prng(uint8_t *dest, unsigned size) {
    for (unsigned i = 0; i < (size + 3) / 4; i++) {
        uint32_t rand = xorshift32();
        for (unsigned j = 0; j < 4; j++) {
            unsigned idx = i * 4 + j;
            if (idx < size) {
                dest[idx] = (uint8_t)((rand >> 8 * j) & 0xff);
            }
        }
    }
    return 1;
}

int main(void) {
    uECC_set_rng(&uECC_prng);

    //uECC_Curve secp256r1 = uECC_secp256r1();
	//uECC_shared_secret(NULL, NULL, NULL, secp256r1);

    platform_init();
    init_uart();
    trigger_setup();
    simpleserial_init();
    simpleserial_addcmd('i', MAX_SS_LEN, cmd_init_prng);

    while(simpleserial_get());

    return 0;
}

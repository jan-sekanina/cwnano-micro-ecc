/* Copyright 2014, Kenneth MacKay. Licensed under the BSD 2-clause license. */

#include "uECC.h"
#include "uECC_vli.h"
#include "hal/hal.h"

/* Counts the number of bits required to represent vli. */
uECC_VLI_API bitcount_t uECC_numBits(const uECC_word_t *vli, const wordcount_t max_words) {
    uECC_word_t i;
    uECC_word_t digit;

    wordcount_t num_digits = vli_numDigits(vli, max_words);
    if (num_digits == 0) {
        return 0;
    }

    digit = vli[num_digits - 1];
    for (i = 0; digit; ++i) {
        NOP_2();
        digit >>= 1;
        NOP_2();
    }

    return (((bitcount_t)(num_digits - 1) << uECC_WORD_BITS_SHIFT) + i);
}

static int uECC_sign_with_k_internal(const uint8_t *private_key,
                                     const uint8_t *message_hash,
                                     unsigned hash_size,
                                     uECC_word_t *k,
                                     uint8_t *signature,
                                     uECC_Curve curve) {

    uECC_word_t tmp[uECC_MAX_WORDS];
    uECC_word_t s[uECC_MAX_WORDS];
    uECC_word_t *initial_Z = 0;
#if uECC_VLI_NATIVE_LITTLE_ENDIAN
    uECC_word_t *p = (uECC_word_t *)signature;
#else
    uECC_word_t p[uECC_MAX_WORDS * 2];
#endif
    wordcount_t num_words = curve->num_words;
    wordcount_t num_n_words = BITS_TO_WORDS(curve->num_n_bits);

    /* Make sure 0 < k < curve_n */
    if (uECC_vli_isZero(k, num_words) || uECC_vli_cmp(curve->n, k, num_n_words) != 1) {
        return 0;
    }

    bitcount_t klen = uECC_numBits(k, num_n_words);
    EccPoint_mult(p, curve->G, k, initial_Z, klen, curve);
    if (uECC_vli_isZero(p, num_words)) {
        return 0;
    }

    uECC_vli_modInv(k, k, curve->n, num_n_words);       /* k = 1 / k */

#if uECC_VLI_NATIVE_LITTLE_ENDIAN == 0
    uECC_vli_nativeToBytes(signature, curve->num_bytes, p); /* store r */
#endif

#if uECC_VLI_NATIVE_LITTLE_ENDIAN
    bcopy((uint8_t *) tmp, private_key, BITS_TO_BYTES(curve->num_n_bits));
#else
    uECC_vli_bytesToNative(tmp, private_key, BITS_TO_BYTES(curve->num_n_bits)); /* tmp = d */
#endif

    s[num_n_words - 1] = 0;
    uECC_vli_set(s, p, num_words);
    uECC_vli_modMult(s, tmp, s, curve->n, num_n_words); /* s = r*d */

    bits2int(tmp, message_hash, hash_size, curve);
    uECC_vli_modAdd(s, tmp, s, curve->n, num_n_words); /* s = e + r*d */
    uECC_vli_modMult(s, s, k, curve->n, num_n_words);  /* s = (e + r*d) / k */
    if (uECC_vli_numBits(s, num_n_words) > (bitcount_t) curve->num_bytes * 8) {
        return 0;
    }
#if uECC_VLI_NATIVE_LITTLE_ENDIAN
    bcopy((uint8_t *) signature + curve->num_bytes, (uint8_t *) s, curve->num_bytes);
#else
    uECC_vli_nativeToBytes(signature + curve->num_bytes, curve->num_bytes, s);
#endif
    return 1;
}

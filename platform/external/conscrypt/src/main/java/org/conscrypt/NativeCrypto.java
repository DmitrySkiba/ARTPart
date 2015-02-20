/*
 * Copyright (C) 2008 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.conscrypt;

import java.io.FileDescriptor;
import java.io.IOException;
import java.io.OutputStream;
import java.net.SocketTimeoutException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;
import java.security.cert.CertificateEncodingException;
import java.security.cert.CertificateException;
import java.security.cert.CertificateParsingException;
import java.security.interfaces.DSAPrivateKey;
import java.security.interfaces.ECPrivateKey;
import java.security.interfaces.RSAPrivateKey;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.net.ssl.SSLException;
import javax.security.auth.x500.X500Principal;

/**
 * Provides the Java side of our JNI glue for OpenSSL.
 */
public final class NativeCrypto {

    // --- OpenSSL library initialization --------------------------------------
    static {
        /*
         * If we're compiled as part of Android, should use a different JNI
         * library name. Detect this by looking for the jarjar'd package name.
         */
        if ("com.android.org.conscrypt".equals(NativeCrypto.class.getPackage().getName())) {
            System.loadLibrary("javacrypto");
        } else if ("com.google.android.gms.org.conscrypt".equals(NativeCrypto.class.getPackage().getName())) {
            System.loadLibrary("gmscore");
            System.loadLibrary("conscrypt_gmscore_jni");
        } else {
            System.loadLibrary("conscrypt_jni");
        }

        clinit();
    }

    private native static void clinit();

    // --- ENGINE functions ----------------------------------------------------
    public static native void ENGINE_load_dynamic();

    public static native long ENGINE_by_id(String id);

    public static native int ENGINE_add(long e);

    public static native int ENGINE_init(long e);

    public static native int ENGINE_finish(long e);

    public static native int ENGINE_free(long e);

    public static native long ENGINE_load_private_key(long e, String key_id);

    public static native String ENGINE_get_id(long engineRef);

    public static native int ENGINE_ctrl_cmd_string(long engineRef, String cmd, String arg,
            int cmd_optional);

    // --- DSA/RSA public/private key handling functions -----------------------

    public static native long EVP_PKEY_new_DSA(byte[] p, byte[] q, byte[] g,
                                               byte[] pub_key, byte[] priv_key);

    public static native long EVP_PKEY_new_RSA(byte[] n, byte[] e, byte[] d, byte[] p, byte[] q,
            byte[] dmp1, byte[] dmq1, byte[] iqmp);

    public static native long EVP_PKEY_new_mac_key(int type, byte[] key);

    public static native int EVP_PKEY_size(long pkey);

    public static native int EVP_PKEY_type(long pkey);

    public static native String EVP_PKEY_print_public(long pkeyRef);

    public static native String EVP_PKEY_print_private(long pkeyRef);

    public static native void EVP_PKEY_free(long pkey);

    public static native int EVP_PKEY_cmp(long pkey1, long pkey2);

    public static native byte[] i2d_PKCS8_PRIV_KEY_INFO(long pkey);

    public static native long d2i_PKCS8_PRIV_KEY_INFO(byte[] data);

    public static native byte[] i2d_PUBKEY(long pkey);

    public static native long d2i_PUBKEY(byte[] data);

    public static native long getRSAPrivateKeyWrapper(RSAPrivateKey key, byte[] modulus);

    public static native long getDSAPrivateKeyWrapper(DSAPrivateKey key);

    public static native long getECPrivateKeyWrapper(ECPrivateKey key, long ecGroupRef);

    public static native long RSA_generate_key_ex(int modulusBits, byte[] publicExponent);

    public static native int RSA_size(long pkey);

    public static native int RSA_private_encrypt(int flen, byte[] from, byte[] to, long pkey,
            int padding);

    public static native int RSA_public_decrypt(int flen, byte[] from, byte[] to, long pkey,
            int padding) throws BadPaddingException, SignatureException;

    public static native int RSA_public_encrypt(int flen, byte[] from, byte[] to, long pkey,
            int padding);

    public static native int RSA_private_decrypt(int flen, byte[] from, byte[] to, long pkey,
            int padding) throws BadPaddingException, SignatureException;

    /**
     * @return array of {n, e}
     */
    public static native byte[][] get_RSA_public_params(long rsa);

    /**
     * @return array of {n, e, d, p, q, dmp1, dmq1, iqmp}
     */
    public static native byte[][] get_RSA_private_params(long rsa);

    public static native long DSA_generate_key(int primeBits, byte[] seed, byte[] g, byte[] p,
            byte[] q);

    /**
     * @return array of {g, p, q, y(pub), x(priv)}
     */
    public static native byte[][] get_DSA_params(long dsa);

    public static native void set_DSA_flag_nonce_from_hash(long dsa);

    public static native byte[] i2d_RSAPublicKey(long rsa);

    public static native byte[] i2d_RSAPrivateKey(long rsa);

    public static native byte[] i2d_DSAPublicKey(long dsa);

    public static native byte[] i2d_DSAPrivateKey(long dsa);

    // --- DH public/private key handling functions ----------------------------

    public static native long EVP_PKEY_new_DH(byte[] p, byte[] g, byte[] pub_key, byte[] priv_key);

    public static native long DH_generate_parameters_ex(int primeBits, long generator);

    public static native void DH_generate_key(long pkeyRef);

    /**
     * @return array of {p, g, y(pub), x(priv)}
     */
    public static native byte[][] get_DH_params(long dh);

    // --- EC functions --------------------------

    /**
     * Used to request EC_GROUP_new_curve_GFp to EC_GROUP_new_curve
     */
    public static final int EC_CURVE_GFP = 1;

    /**
     * Used to request EC_GROUP_new_curve_GF2m to EC_GROUP_new_curve
     */
    public static final int EC_CURVE_GF2M = 2;

    /**
     * EC_GROUP_set_asn1_flag: indicates an EC_GROUP is a NamedCurve.
     */
    public static final int OPENSSL_EC_NAMED_CURVE = 0x001;

    /**
     * EC_GROUP_set_point_conversion_form: indicates compressed ASN.1 format
     */
    public static final int POINT_CONVERSION_COMPRESSED = 2;

    /**
     * EC_GROUP_set_point_conversion_form: indicates uncompressed ASN.1 format
     */
    public static final int POINT_CONVERSION_UNCOMPRESSED = 4;

    /**
     * EC_GROUP_set_point_conversion_form: indicates hybrid ASN.1 format
     */
    public static final int POINT_CONVERSION_HYBRID = 4;

    public static native long EVP_PKEY_new_EC_KEY(long groupRef, long pubkeyRef, byte[] privkey);

    public static native long EC_GROUP_new_by_curve_name(String curveName);

    public static native long EC_GROUP_new_curve(int type, byte[] p, byte[] a, byte[] b);

    public static native long EC_GROUP_dup(long groupRef);

    public static native void EC_GROUP_set_asn1_flag(long groupRef, int flag);

    public static native void EC_GROUP_set_point_conversion_form(long groupRef, int form);

    public static native String EC_GROUP_get_curve_name(long groupRef);

    public static native byte[][] EC_GROUP_get_curve(long groupRef);

    public static native void EC_GROUP_clear_free(long ctx);

    public static native boolean EC_GROUP_cmp(long ctx1, long ctx2);

    public static native void EC_GROUP_set_generator(long groupCtx, long pointCtx, byte[] n, byte[] h);

    public static native long EC_GROUP_get_generator(long groupCtx);

    public static native int get_EC_GROUP_type(long groupCtx);

    public static native byte[] EC_GROUP_get_order(long groupCtx);

    public static native int EC_GROUP_get_degree(long groupCtx);

    public static native byte[] EC_GROUP_get_cofactor(long groupCtx);

    public static native long EC_POINT_new(long groupRef);

    public static native void EC_POINT_clear_free(long pointRef);

    public static native boolean EC_POINT_cmp(long groupRef, long pointRef1, long pointRef2);

    public static native byte[][] EC_POINT_get_affine_coordinates(long groupCtx, long pointCtx);

    public static native void EC_POINT_set_affine_coordinates(long groupCtx, long pointCtx, byte[] x,
            byte[] y);

    public static native long EC_KEY_generate_key(long groupRef);

    public static native long EC_KEY_get0_group(long pkeyRef);

    public static native byte[] EC_KEY_get_private_key(long keyRef);

    public static native long EC_KEY_get_public_key(long keyRef);

    public static native void EC_KEY_set_nonce_from_hash(long keyRef, boolean enabled);

    public static native int ECDH_compute_key(
            byte[] out, int outOffset, long publicKeyRef, long privateKeyRef);

    // --- Message digest functions --------------

    public static native long EVP_get_digestbyname(String name);

    public static native int EVP_MD_size(long evp_md);

    public static native int EVP_MD_block_size(long evp_md);

    // --- Message digest context functions --------------

    public static native long EVP_MD_CTX_create();

    public static native void EVP_MD_CTX_init(OpenSSLDigestContext ctx);

    public static native void EVP_MD_CTX_destroy(long ctx);

    public static native int EVP_MD_CTX_copy(OpenSSLDigestContext dst_ctx,
            OpenSSLDigestContext src_ctx);

    // --- Digest handling functions -------------------------------------------

    public static native int EVP_DigestInit(OpenSSLDigestContext ctx, long evp_md);

    public static native void EVP_DigestUpdate(OpenSSLDigestContext ctx, byte[] buffer,
            int offset, int length);

    public static native int EVP_DigestFinal(OpenSSLDigestContext ctx, byte[] hash, int offset);

    // --- MAC handling functions ----------------------------------------------

    public static native void EVP_DigestSignInit(OpenSSLDigestContext evp_md_ctx, long evp_md,
            long evp_pkey);

    public static native void EVP_DigestSignUpdate(OpenSSLDigestContext evp_md_ctx, byte[] in);

    public static native byte[] EVP_DigestSignFinal(OpenSSLDigestContext evp_md_ctx);

    // --- Signature handling functions ----------------------------------------

    public static native int EVP_SignInit(OpenSSLDigestContext ctx, long evpRef);

    public static native void EVP_SignUpdate(OpenSSLDigestContext ctx, byte[] buffer,
                                               int offset, int length);

    public static native int EVP_SignFinal(OpenSSLDigestContext ctx, byte[] signature, int offset,
            long key);

    public static native int EVP_VerifyInit(OpenSSLDigestContext ctx, long evpRef);

    public static native void EVP_VerifyUpdate(OpenSSLDigestContext ctx, byte[] buffer,
                                               int offset, int length);

    public static native int EVP_VerifyFinal(OpenSSLDigestContext ctx, byte[] signature,
                                             int offset, int length, long key);


    // --- Block ciphers -------------------------------------------------------

    public static native long EVP_get_cipherbyname(String string);

    public static native void EVP_CipherInit_ex(long ctx, long evpCipher, byte[] key, byte[] iv,
            boolean encrypting);

    public static native int EVP_CipherUpdate(long ctx, byte[] out, int outOffset, byte[] in,
            int inOffset, int inLength);

    public static native int EVP_CipherFinal_ex(long ctx, byte[] out, int outOffset)
            throws BadPaddingException, IllegalBlockSizeException;

    public static native int EVP_CIPHER_iv_length(long evpCipher);

    public static native long EVP_CIPHER_CTX_new();

    public static native int EVP_CIPHER_CTX_block_size(long ctx);

    public static native int get_EVP_CIPHER_CTX_buf_len(long ctx);

    public static native void EVP_CIPHER_CTX_set_padding(long ctx, boolean enablePadding);

    public static native void EVP_CIPHER_CTX_set_key_length(long ctx, int keyBitSize);

    public static native void EVP_CIPHER_CTX_cleanup(long ctx);

    // --- RAND seeding --------------------------------------------------------

    public static final int RAND_SEED_LENGTH_IN_BYTES = 1024;

    public static native void RAND_seed(byte[] seed);

    public static native int RAND_load_file(String filename, long max_bytes);

    public static native void RAND_bytes(byte[] output);

    // --- ASN.1 objects -------------------------------------------------------

    public static native int OBJ_txt2nid(String oid);

    public static native String OBJ_txt2nid_longName(String oid);

    public static native String OBJ_txt2nid_oid(String oid);

    // --- X509_NAME -----------------------------------------------------------

    public static int X509_NAME_hash(X500Principal principal) {
        return X509_NAME_hash(principal, "SHA1");
    }
    public static int X509_NAME_hash_old(X500Principal principal) {
        return X509_NAME_hash(principal, "MD5");
    }
    private static int X509_NAME_hash(X500Principal principal, String algorithm) {
        try {
            byte[] digest = MessageDigest.getInstance(algorithm).digest(principal.getEncoded());
            int offset = 0;
            return (((digest[offset++] & 0xff) <<  0) |
                    ((digest[offset++] & 0xff) <<  8) |
                    ((digest[offset++] & 0xff) << 16) |
                    ((digest[offset  ] & 0xff) << 24));
        } catch (NoSuchAlgorithmException e) {
            throw new AssertionError(e);
        }
    }

    public static native String X509_NAME_print_ex(long x509nameCtx, long flags);

    // --- X509 ----------------------------------------------------------------

    /** Used to request get_X509_GENERAL_NAME_stack get the "altname" field. */
    public static final int GN_STACK_SUBJECT_ALT_NAME = 1;

    /**
     * Used to request get_X509_GENERAL_NAME_stack get the issuerAlternativeName
     * extension.
     */
    public static final int GN_STACK_ISSUER_ALT_NAME = 2;

    /**
     * Used to request only non-critical types in get_X509*_ext_oids.
     */
    public static final int EXTENSION_TYPE_NON_CRITICAL = 0;

    /**
     * Used to request only critical types in get_X509*_ext_oids.
     */
    public static final int EXTENSION_TYPE_CRITICAL = 1;

    public static native long d2i_X509_bio(long bioCtx);

    public static native long d2i_X509(byte[] encoded);

    public static native long PEM_read_bio_X509(long bioCtx);

    public static native byte[] i2d_X509(long x509ctx);

    /** Takes an X509 context not an X509_PUBKEY context. */
    public static native byte[] i2d_X509_PUBKEY(long x509ctx);

    public static native byte[] ASN1_seq_pack_X509(long[] x509CertRefs);

    public static native long[] ASN1_seq_unpack_X509_bio(long bioRef);

    public static native void X509_free(long x509ctx);

    public static native int X509_cmp(long x509ctx1, long x509ctx2);

    public static native int get_X509_hashCode(long x509ctx);

    public static native void X509_print_ex(long bioCtx, long x509ctx, long nmflag, long certflag);

    public static native byte[] X509_get_issuer_name(long x509ctx);

    public static native byte[] X509_get_subject_name(long x509ctx);

    public static native String get_X509_sig_alg_oid(long x509ctx);

    public static native byte[] get_X509_sig_alg_parameter(long x509ctx);

    public static native boolean[] get_X509_issuerUID(long x509ctx);

    public static native boolean[] get_X509_subjectUID(long x509ctx);

    public static native long X509_get_pubkey(long x509ctx) throws NoSuchAlgorithmException;

    public static native String get_X509_pubkey_oid(long x509ctx);

    public static native byte[] X509_get_ext_oid(long x509ctx, String oid);

    public static native String[] get_X509_ext_oids(long x509ctx, int critical);

    public static native Object[][] get_X509_GENERAL_NAME_stack(long x509ctx, int type)
            throws CertificateParsingException;

    public static native boolean[] get_X509_ex_kusage(long x509ctx);

    public static native String[] get_X509_ex_xkusage(long x509ctx);

    public static native int get_X509_ex_pathlen(long x509ctx);

    public static native long X509_get_notBefore(long x509ctx);

    public static native long X509_get_notAfter(long x509ctx);

    public static native long X509_get_version(long x509ctx);

    public static native byte[] X509_get_serialNumber(long x509ctx);

    public static native void X509_verify(long x509ctx, long pkeyCtx) throws BadPaddingException;

    public static native byte[] get_X509_cert_info_enc(long x509ctx);

    public static native byte[] get_X509_signature(long x509ctx);

    public static native int get_X509_ex_flags(long x509ctx);

    public static native int X509_check_issued(long ctx, long ctx2);

    // --- X509 EXFLAG ---------------------------------------------------------

    public static final int EXFLAG_CA = 0x10;

    public static final int EXFLAG_CRITICAL = 0x200;

    // --- PKCS7 ---------------------------------------------------------------

    /** Used as the "which" field in d2i_PKCS7_bio and PEM_read_bio_PKCS7. */
    public static final int PKCS7_CERTS = 1;

    /** Used as the "which" field in d2i_PKCS7_bio and PEM_read_bio_PKCS7. */
    public static final int PKCS7_CRLS = 2;

    /** Returns an array of X509 or X509_CRL pointers. */
    public static native long[] d2i_PKCS7_bio(long bioCtx, int which);

    /** Returns an array of X509 or X509_CRL pointers. */
    public static native byte[] i2d_PKCS7(long[] certs);

    /** Returns an array of X509 or X509_CRL pointers. */
    public static native long[] PEM_read_bio_PKCS7(long bioCtx, int which);

    // --- X509_CRL ------------------------------------------------------------

    public static native long d2i_X509_CRL_bio(long bioCtx);

    public static native long PEM_read_bio_X509_CRL(long bioCtx);

    public static native byte[] i2d_X509_CRL(long x509CrlCtx);

    public static native void X509_CRL_free(long x509CrlCtx);

    public static native void X509_CRL_print(long bioCtx, long x509CrlCtx);

    public static native String get_X509_CRL_sig_alg_oid(long x509CrlCtx);

    public static native byte[] get_X509_CRL_sig_alg_parameter(long x509CrlCtx);

    public static native byte[] X509_CRL_get_issuer_name(long x509CrlCtx);

    /** Returns X509_REVOKED reference that is not duplicated! */
    public static native long X509_CRL_get0_by_cert(long x509CrlCtx, long x509Ctx);

    /** Returns X509_REVOKED reference that is not duplicated! */
    public static native long X509_CRL_get0_by_serial(long x509CrlCtx, byte[] serial);

    /** Returns an array of X509_REVOKED that are owned by the caller. */
    public static native long[] X509_CRL_get_REVOKED(long x509CrlCtx);

    public static native String[] get_X509_CRL_ext_oids(long x509ctx, int critical);

    public static native byte[] X509_CRL_get_ext_oid(long x509CrlCtx, String oid);

    public static native long X509_CRL_get_version(long x509CrlCtx);

    public static native long X509_CRL_get_ext(long x509CrlCtx, String oid);

    public static native byte[] get_X509_CRL_signature(long x509ctx);

    public static native void X509_CRL_verify(long x509CrlCtx, long pkeyCtx);

    public static native byte[] get_X509_CRL_crl_enc(long x509CrlCtx);

    public static native long X509_CRL_get_lastUpdate(long x509CrlCtx);

    public static native long X509_CRL_get_nextUpdate(long x509CrlCtx);

    // --- X509_REVOKED --------------------------------------------------------

    public static native long X509_REVOKED_dup(long x509RevokedCtx);

    public static native byte[] i2d_X509_REVOKED(long x509RevokedCtx);

    public static native String[] get_X509_REVOKED_ext_oids(long x509ctx, int critical);

    public static native byte[] X509_REVOKED_get_ext_oid(long x509RevokedCtx, String oid);

    public static native byte[] X509_REVOKED_get_serialNumber(long x509RevokedCtx);

    public static native long X509_REVOKED_get_ext(long x509RevokedCtx, String oid);

    /** Returns ASN1_TIME reference. */
    public static native long get_X509_REVOKED_revocationDate(long x509RevokedCtx);

    public static native void X509_REVOKED_print(long bioRef, long x509RevokedCtx);

    // --- X509_EXTENSION ------------------------------------------------------

    public static native int X509_supported_extension(long x509ExtensionRef);

    // --- ASN1_TIME -----------------------------------------------------------

    public static native void ASN1_TIME_to_Calendar(long asn1TimeCtx, Calendar cal);

    // --- BIO stream creation -------------------------------------------------

    public static native long create_BIO_InputStream(OpenSSLBIOInputStream is);

    public static native long create_BIO_OutputStream(OutputStream os);

    public static native int BIO_read(long bioRef, byte[] buffer);

    public static native void BIO_write(long bioRef, byte[] buffer, int offset, int length)
            throws IOException;

    public static native void BIO_free_all(long bioRef);

    // --- SSL handling --------------------------------------------------------

    private static final String SUPPORTED_PROTOCOL_SSLV3 = "SSLv3";
    private static final String SUPPORTED_PROTOCOL_TLSV1 = "TLSv1";
    private static final String SUPPORTED_PROTOCOL_TLSV1_1 = "TLSv1.1";
    private static final String SUPPORTED_PROTOCOL_TLSV1_2 = "TLSv1.2";

    public static final Map<String, String> OPENSSL_TO_STANDARD_CIPHER_SUITES
            = new HashMap<String, String>();
    public static final Map<String, String> STANDARD_TO_OPENSSL_CIPHER_SUITES
            = new LinkedHashMap<String, String>();

    private static void add(String standard, String openssl) {
        OPENSSL_TO_STANDARD_CIPHER_SUITES.put(openssl, standard);
        STANDARD_TO_OPENSSL_CIPHER_SUITES.put(standard, openssl);
    }

    /**
     * TLS_EMPTY_RENEGOTIATION_INFO_SCSV is RFC 5746's renegotiation
     * indication signaling cipher suite value. It is not a real
     * cipher suite. It is just an indication in the default and
     * supported cipher suite lists indicates that the implementation
     * supports secure renegotiation.
     *
     * In the RI, its presence means that the SCSV is sent in the
     * cipher suite list to indicate secure renegotiation support and
     * its absense means to send an empty TLS renegotiation info
     * extension instead.
     *
     * However, OpenSSL doesn't provide an API to give this level of
     * control, instead always sending the SCSV and always including
     * the empty renegotiation info if TLS is used (as opposed to
     * SSL). So we simply allow TLS_EMPTY_RENEGOTIATION_INFO_SCSV to
     * be passed for compatibility as to provide the hint that we
     * support secure renegotiation.
     */
    public static final String TLS_EMPTY_RENEGOTIATION_INFO_SCSV
            = "TLS_EMPTY_RENEGOTIATION_INFO_SCSV";

    /**
     * TLS_FALLBACK_SCSV is from
     * https://tools.ietf.org/html/draft-ietf-tls-downgrade-scsv-00
     * to indicate to the server that this is a fallback protocol
     * request.
     */
    public static final String TLS_FALLBACK_SCSV = "TLS_FALLBACK_SCSV";

    static {
        add("SSL_RSA_WITH_RC4_128_MD5",              "RC4-MD5");
        add("SSL_RSA_WITH_RC4_128_SHA",              "RC4-SHA");
        add("TLS_RSA_WITH_AES_128_CBC_SHA",          "AES128-SHA");
        add("TLS_RSA_WITH_AES_256_CBC_SHA",          "AES256-SHA");
        add("TLS_ECDH_ECDSA_WITH_RC4_128_SHA",       "ECDH-ECDSA-RC4-SHA");
        add("TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA",   "ECDH-ECDSA-AES128-SHA");
        add("TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA",   "ECDH-ECDSA-AES256-SHA");
        add("TLS_ECDH_RSA_WITH_RC4_128_SHA",         "ECDH-RSA-RC4-SHA");
        add("TLS_ECDH_RSA_WITH_AES_128_CBC_SHA",     "ECDH-RSA-AES128-SHA");
        add("TLS_ECDH_RSA_WITH_AES_256_CBC_SHA",     "ECDH-RSA-AES256-SHA");
        add("TLS_ECDHE_ECDSA_WITH_RC4_128_SHA",      "ECDHE-ECDSA-RC4-SHA");
        add("TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",  "ECDHE-ECDSA-AES128-SHA");
        add("TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",  "ECDHE-ECDSA-AES256-SHA");
        add("TLS_ECDHE_RSA_WITH_RC4_128_SHA",        "ECDHE-RSA-RC4-SHA");
        add("TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",    "ECDHE-RSA-AES128-SHA");
        add("TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",    "ECDHE-RSA-AES256-SHA");
        add("TLS_DHE_RSA_WITH_AES_128_CBC_SHA",      "DHE-RSA-AES128-SHA");
        add("TLS_DHE_RSA_WITH_AES_256_CBC_SHA",      "DHE-RSA-AES256-SHA");
        add("TLS_DHE_DSS_WITH_AES_128_CBC_SHA",      "DHE-DSS-AES128-SHA");
        add("TLS_DHE_DSS_WITH_AES_256_CBC_SHA",      "DHE-DSS-AES256-SHA");
        add("SSL_RSA_WITH_3DES_EDE_CBC_SHA",         "DES-CBC3-SHA");
        add("TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA",  "ECDH-ECDSA-DES-CBC3-SHA");
        add("TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA",    "ECDH-RSA-DES-CBC3-SHA");
        add("TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA", "ECDHE-ECDSA-DES-CBC3-SHA");
        add("TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA",   "ECDHE-RSA-DES-CBC3-SHA");
        add("SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA",     "EDH-RSA-DES-CBC3-SHA");
        add("SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA",     "EDH-DSS-DES-CBC3-SHA");
        add("SSL_RSA_WITH_DES_CBC_SHA",              "DES-CBC-SHA");
        add("SSL_DHE_RSA_WITH_DES_CBC_SHA",          "EDH-RSA-DES-CBC-SHA");
        add("SSL_DHE_DSS_WITH_DES_CBC_SHA",          "EDH-DSS-DES-CBC-SHA");
        add("SSL_RSA_EXPORT_WITH_RC4_40_MD5",        "EXP-RC4-MD5");
        add("SSL_RSA_EXPORT_WITH_DES40_CBC_SHA",     "EXP-DES-CBC-SHA");
        add("SSL_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA", "EXP-EDH-RSA-DES-CBC-SHA");
        add("SSL_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA", "EXP-EDH-DSS-DES-CBC-SHA");
        add("SSL_RSA_WITH_NULL_MD5",                 "NULL-MD5");
        add("SSL_RSA_WITH_NULL_SHA",                 "NULL-SHA");
        add("TLS_ECDH_ECDSA_WITH_NULL_SHA",          "ECDH-ECDSA-NULL-SHA");
        add("TLS_ECDH_RSA_WITH_NULL_SHA",            "ECDH-RSA-NULL-SHA");
        add("TLS_ECDHE_ECDSA_WITH_NULL_SHA",         "ECDHE-ECDSA-NULL-SHA");
        add("TLS_ECDHE_RSA_WITH_NULL_SHA",           "ECDHE-RSA-NULL-SHA");
        add("SSL_DH_anon_WITH_RC4_128_MD5",          "ADH-RC4-MD5");
        add("TLS_DH_anon_WITH_AES_128_CBC_SHA",      "ADH-AES128-SHA");
        add("TLS_DH_anon_WITH_AES_256_CBC_SHA",      "ADH-AES256-SHA");
        add("SSL_DH_anon_WITH_3DES_EDE_CBC_SHA",     "ADH-DES-CBC3-SHA");
        add("SSL_DH_anon_WITH_DES_CBC_SHA",          "ADH-DES-CBC-SHA");
        add("TLS_ECDH_anon_WITH_RC4_128_SHA",        "AECDH-RC4-SHA");
        add("TLS_ECDH_anon_WITH_AES_128_CBC_SHA",    "AECDH-AES128-SHA");
        add("TLS_ECDH_anon_WITH_AES_256_CBC_SHA",    "AECDH-AES256-SHA");
        add("TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA",   "AECDH-DES-CBC3-SHA");
        add("SSL_DH_anon_EXPORT_WITH_RC4_40_MD5",    "EXP-ADH-RC4-MD5");
        add("SSL_DH_anon_EXPORT_WITH_DES40_CBC_SHA", "EXP-ADH-DES-CBC-SHA");
        add("TLS_ECDH_anon_WITH_NULL_SHA",           "AECDH-NULL-SHA");

        // TLSv1.2 cipher suites
        add("TLS_RSA_WITH_NULL_SHA256",                "NULL-SHA256");
        add("TLS_RSA_WITH_AES_128_CBC_SHA256",         "AES128-SHA256");
        add("TLS_RSA_WITH_AES_256_CBC_SHA256",         "AES256-SHA256");
        add("TLS_RSA_WITH_AES_128_GCM_SHA256",         "AES128-GCM-SHA256");
        add("TLS_RSA_WITH_AES_256_GCM_SHA384",         "AES256-GCM-SHA384");
        add("TLS_DHE_RSA_WITH_AES_128_CBC_SHA256",     "DHE-RSA-AES128-SHA256");
        add("TLS_DHE_RSA_WITH_AES_256_CBC_SHA256",     "DHE-RSA-AES256-SHA256");
        add("TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",     "DHE-RSA-AES128-GCM-SHA256");
        add("TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",     "DHE-RSA-AES256-GCM-SHA384");
        add("TLS_DHE_DSS_WITH_AES_128_CBC_SHA256",     "DHE-DSS-AES128-SHA256");
        add("TLS_DHE_DSS_WITH_AES_256_CBC_SHA256",     "DHE-DSS-AES256-SHA256");
        add("TLS_DHE_DSS_WITH_AES_128_GCM_SHA256",     "DHE-DSS-AES128-GCM-SHA256");
        add("TLS_DHE_DSS_WITH_AES_256_GCM_SHA384",     "DHE-DSS-AES256-GCM-SHA384");
        add("TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256",    "ECDH-RSA-AES128-SHA256");
        add("TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384",    "ECDH-RSA-AES256-SHA384");
        add("TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256",    "ECDH-RSA-AES128-GCM-SHA256");
        add("TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384",    "ECDH-RSA-AES256-GCM-SHA384");
        add("TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256",  "ECDH-ECDSA-AES128-SHA256");
        add("TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384",  "ECDH-ECDSA-AES256-SHA384");
        add("TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256",  "ECDH-ECDSA-AES128-GCM-SHA256");
        add("TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384",  "ECDH-ECDSA-AES256-GCM-SHA384");
        add("TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",   "ECDHE-RSA-AES128-SHA256");
        add("TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",   "ECDHE-RSA-AES256-SHA384");
        add("TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",   "ECDHE-RSA-AES128-GCM-SHA256");
        add("TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",   "ECDHE-RSA-AES256-GCM-SHA384");
        add("TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256", "ECDHE-ECDSA-AES128-SHA256");
        add("TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384", "ECDHE-ECDSA-AES256-SHA384");
        add("TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256", "ECDHE-ECDSA-AES128-GCM-SHA256");
        add("TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384", "ECDHE-ECDSA-AES256-GCM-SHA384");
        add("TLS_DH_anon_WITH_AES_128_CBC_SHA256",     "ADH-AES128-SHA256");
        add("TLS_DH_anon_WITH_AES_256_CBC_SHA256",     "ADH-AES256-SHA256");
        add("TLS_DH_anon_WITH_AES_128_GCM_SHA256",     "ADH-AES128-GCM-SHA256");
        add("TLS_DH_anon_WITH_AES_256_GCM_SHA384",     "ADH-AES256-GCM-SHA384");

        // No Kerberos in Android
        // add("TLS_KRB5_WITH_RC4_128_SHA",           "KRB5-RC4-SHA");
        // add("TLS_KRB5_WITH_RC4_128_MD5",           "KRB5-RC4-MD5");
        // add("TLS_KRB5_WITH_3DES_EDE_CBC_SHA",      "KRB5-DES-CBC3-SHA");
        // add("TLS_KRB5_WITH_3DES_EDE_CBC_MD5",      "KRB5-DES-CBC3-MD5");
        // add("TLS_KRB5_WITH_DES_CBC_SHA",           "KRB5-DES-CBC-SHA");
        // add("TLS_KRB5_WITH_DES_CBC_MD5",           "KRB5-DES-CBC-MD5");
        // add("TLS_KRB5_EXPORT_WITH_RC4_40_SHA",     "EXP-KRB5-RC4-SHA");
        // add("TLS_KRB5_EXPORT_WITH_RC4_40_MD5",     "EXP-KRB5-RC4-MD5");
        // add("TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA", "EXP-KRB5-DES-CBC-SHA");
        // add("TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5", "EXP-KRB5-DES-CBC-MD5");

        // not implemented by either RI or OpenSSL
        // add("SSL_DH_DSS_EXPORT_WITH_DES40_CBC_SHA", null);
        // add("SSL_DH_RSA_EXPORT_WITH_DES40_CBC_SHA", null);

        // EXPORT1024 suites were never standardized but were widely implemented.
        // OpenSSL 0.9.8c and later have disabled TLS1_ALLOW_EXPERIMENTAL_CIPHERSUITES
        // add("SSL_RSA_EXPORT1024_WITH_DES_CBC_SHA", "EXP1024-DES-CBC-SHA");
        // add("SSL_RSA_EXPORT1024_WITH_RC4_56_SHA",  "EXP1024-RC4-SHA");

        // No RC2
        // add("SSL_RSA_EXPORT_WITH_RC2_CBC_40_MD5",  "EXP-RC2-CBC-MD5");
        // add("TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA", "EXP-KRB5-RC2-CBC-SHA");
        // add("TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5", "EXP-KRB5-RC2-CBC-MD5");

        // Pre-Shared Key (PSK) cipher suites
        add("TLS_PSK_WITH_3DES_EDE_CBC_SHA", "PSK-3DES-EDE-CBC-SHA");
        add("TLS_PSK_WITH_AES_128_CBC_SHA", "PSK-AES128-CBC-SHA");
        add("TLS_PSK_WITH_AES_256_CBC_SHA", "PSK-AES256-CBC-SHA");
        add("TLS_PSK_WITH_RC4_128_SHA", "PSK-RC4-SHA");
        add("TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA", "ECDHE-PSK-AES128-CBC-SHA");
        add("TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA", "ECDHE-PSK-AES256-CBC-SHA");

        // Signaling Cipher Suite Value for secure renegotiation handled as special case.
        // add("TLS_EMPTY_RENEGOTIATION_INFO_SCSV", null);

        // Similarly, the fallback SCSV is handled as a special case.
        // add("TLS_FALLBACK_SCSV", null);
    }

    private static final String[] SUPPORTED_CIPHER_SUITES;
    static {
        int size = STANDARD_TO_OPENSSL_CIPHER_SUITES.size();
        SUPPORTED_CIPHER_SUITES = new String[size + 2];
        STANDARD_TO_OPENSSL_CIPHER_SUITES.keySet().toArray(SUPPORTED_CIPHER_SUITES);
        SUPPORTED_CIPHER_SUITES[size] = TLS_EMPTY_RENEGOTIATION_INFO_SCSV;
        SUPPORTED_CIPHER_SUITES[size + 1] = TLS_FALLBACK_SCSV;
    }

    // EVP_PKEY types from evp.h and objects.h
    public static final int EVP_PKEY_RSA  = 6;   // NID_rsaEcnryption
    public static final int EVP_PKEY_DSA  = 116; // NID_dsa
    public static final int EVP_PKEY_DH   = 28;  // NID_dhKeyAgreement
    public static final int EVP_PKEY_EC   = 408; // NID_X9_62_id_ecPublicKey
    public static final int EVP_PKEY_HMAC = 855; // NID_hmac
    public static final int EVP_PKEY_CMAC = 894; // NID_cmac

    // RSA padding modes from rsa.h
    public static final int RSA_PKCS1_PADDING = 1;
    public static final int RSA_NO_PADDING    = 3;

    // SSL mode from ssl.h
    public static final long SSL_MODE_HANDSHAKE_CUTTHROUGH = 0x00000080L;
    public static final long SSL_MODE_CBC_RECORD_SPLITTING = 0x00000100L;
    public static final long SSL_MODE_SEND_FALLBACK_SCSV   = 0x00000200L;

    // SSL options from ssl.h
    public static final long SSL_OP_TLSEXT_PADDING                         = 0x00000010L;
    public static final long SSL_OP_NO_TICKET                              = 0x00004000L;
    public static final long SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION = 0x00010000L;
    public static final long SSL_OP_NO_SSLv3                               = 0x02000000L;
    public static final long SSL_OP_NO_TLSv1                               = 0x04000000L;
    public static final long SSL_OP_NO_TLSv1_1                             = 0x10000000L;
    public static final long SSL_OP_NO_TLSv1_2                             = 0x08000000L;

    /*
     * Client certificate types as defined in
     * TLS 1.0 spec., 7.4.4. Certificate request.
     * EC constants from RFC 4492.
     * OpenSSL constants from ssl/tls1.h.
     */
    public static final byte TLS_CT_RSA_SIGN = 1;
    public static final byte TLS_CT_DSS_SIGN = 2;
    public static final byte TLS_CT_RSA_FIXED_DH = 3;
    public static final byte TLS_CT_DSS_FIXED_DH = 4;
    public static final byte TLS_CT_ECDSA_SIGN = 64;
    public static final byte TLS_CT_RSA_FIXED_ECDH = 65;
    public static final byte TLS_CT_ECDSA_FIXED_ECDH = 66;

    /*
     * Used in the SSL_get_shutdown and SSL_set_shutdown functions.
     */
    public static final int SSL_SENT_SHUTDOWN = 1;
    public static final int SSL_RECEIVED_SHUTDOWN = 2;

    public static native long SSL_CTX_new();

    // IMPLEMENTATION NOTE: The default list of cipher suites is a trade-off between what we'd like
    // to use and what servers currently support. We strive to be secure enough by default. We thus
    // avoid unacceptably weak suites (e.g., those with bulk cipher secret key shorter than 128
    // bits), while maintaining the capability to connect to the majority of servers.
    //
    // Cipher suites are listed in preference order (favorite choice first) of the client. However,
    // servers are not required to honor the order. The key rules governing the preference order
    // are:
    // * Prefer Forward Secrecy (i.e., cipher suites that use ECDHE and DHE for key agreement).
    // * Prefer AES-GCM to AES-CBC whose MAC-pad-then-encrypt approach leads to weaknesses (e.g.,
    //   Lucky 13).
    // * Prefer AES to RC4 whose foundations are a bit shaky. See http://www.isg.rhul.ac.uk/tls/.
    //   BEAST and Lucky13 mitigations are enabled.
    // * Prefer 128-bit bulk encryption to 256-bit one, because 128-bit is safe enough while
    //   consuming less CPU/time/energy.
    //
    // NOTE: Removing cipher suites from this list needs to be done with caution, because this may
    // prevent apps from connecting to servers they were previously able to connect to.

    /** X.509 based cipher suites enabled by default (if requested), in preference order. */
    static final String[] DEFAULT_X509_CIPHER_SUITES = new String[] {
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
        "TLS_DHE_DSS_WITH_AES_128_CBC_SHA",
        "TLS_DHE_DSS_WITH_AES_256_CBC_SHA",
        "TLS_ECDHE_ECDSA_WITH_RC4_128_SHA",
        "TLS_ECDHE_RSA_WITH_RC4_128_SHA",
        "TLS_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_RSA_WITH_AES_128_CBC_SHA",
        "TLS_RSA_WITH_AES_256_CBC_SHA",
        "SSL_RSA_WITH_RC4_128_SHA",
    };

    /** TLS-PSK cipher suites enabled by default (if requested), in preference order. */
    static final String[] DEFAULT_PSK_CIPHER_SUITES = new String[] {
        "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA",
        "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA",
        "TLS_PSK_WITH_AES_128_CBC_SHA",
        "TLS_PSK_WITH_AES_256_CBC_SHA",
    };

    public static String[] getSupportedCipherSuites() {
        return SUPPORTED_CIPHER_SUITES.clone();
    }

    public static native void SSL_CTX_free(long ssl_ctx);

    public static native void SSL_CTX_set_session_id_context(long ssl_ctx, byte[] sid_ctx);

    public static native long SSL_new(long ssl_ctx) throws SSLException;

    public static native void SSL_enable_tls_channel_id(long ssl) throws SSLException;

    public static native byte[] SSL_get_tls_channel_id(long ssl) throws SSLException;

    public static native void SSL_set1_tls_channel_id(long ssl, long pkey);

    public static native void SSL_use_certificate(long ssl, long[] x509refs);

    public static native void SSL_use_PrivateKey(long ssl, long pkey);

    public static native void SSL_check_private_key(long ssl) throws SSLException;

    public static native void SSL_set_client_CA_list(long ssl, byte[][] asn1DerEncodedX500Principals);

    public static native long SSL_get_mode(long ssl);

    public static native long SSL_set_mode(long ssl, long mode);

    public static native long SSL_clear_mode(long ssl, long mode);

    public static native long SSL_get_options(long ssl);

    public static native long SSL_set_options(long ssl, long options);

    public static native long SSL_clear_options(long ssl, long options);

    public static native void SSL_use_psk_identity_hint(long ssl, String identityHint)
            throws SSLException;

    public static native void set_SSL_psk_client_callback_enabled(long ssl, boolean enabled);

    public static native void set_SSL_psk_server_callback_enabled(long ssl, boolean enabled);

    public static final String[] DEFAULT_PROTOCOLS = new String[] {
        SUPPORTED_PROTOCOL_SSLV3,
        SUPPORTED_PROTOCOL_TLSV1,
        SUPPORTED_PROTOCOL_TLSV1_1,
        SUPPORTED_PROTOCOL_TLSV1_2,
    };

    public static String[] getSupportedProtocols() {
        return new String[] { SUPPORTED_PROTOCOL_SSLV3,
                              SUPPORTED_PROTOCOL_TLSV1,
                              SUPPORTED_PROTOCOL_TLSV1_1,
                              SUPPORTED_PROTOCOL_TLSV1_2,
        };
    }

    public static void setEnabledProtocols(long ssl, String[] protocols) {
        checkEnabledProtocols(protocols);
        // openssl uses negative logic letting you disable protocols.
        // so first, assume we need to set all (disable all) and clear none (enable none).
        // in the loop, selectively move bits from set to clear (from disable to enable)
        long optionsToSet = (SSL_OP_NO_SSLv3 | SSL_OP_NO_TLSv1 | SSL_OP_NO_TLSv1_1 | SSL_OP_NO_TLSv1_2);
        long optionsToClear = 0;
        for (int i = 0; i < protocols.length; i++) {
            String protocol = protocols[i];
            if (protocol.equals(SUPPORTED_PROTOCOL_SSLV3)) {
                optionsToSet &= ~SSL_OP_NO_SSLv3;
                optionsToClear |= SSL_OP_NO_SSLv3;
            } else if (protocol.equals(SUPPORTED_PROTOCOL_TLSV1)) {
                optionsToSet &= ~SSL_OP_NO_TLSv1;
                optionsToClear |= SSL_OP_NO_TLSv1;
            } else if (protocol.equals(SUPPORTED_PROTOCOL_TLSV1_1)) {
                optionsToSet &= ~SSL_OP_NO_TLSv1_1;
                optionsToClear |= SSL_OP_NO_TLSv1_1;
            } else if (protocol.equals(SUPPORTED_PROTOCOL_TLSV1_2)) {
                optionsToSet &= ~SSL_OP_NO_TLSv1_2;
                optionsToClear |= SSL_OP_NO_TLSv1_2;
            } else {
                // error checked by checkEnabledProtocols
                throw new IllegalStateException();
            }
        }

        SSL_set_options(ssl, optionsToSet);
        SSL_clear_options(ssl, optionsToClear);
    }

    public static String[] checkEnabledProtocols(String[] protocols) {
        if (protocols == null) {
            throw new IllegalArgumentException("protocols == null");
        }
        for (int i = 0; i < protocols.length; i++) {
            String protocol = protocols[i];
            if (protocol == null) {
                throw new IllegalArgumentException("protocols[" + i + "] == null");
            }
            if ((!protocol.equals(SUPPORTED_PROTOCOL_SSLV3))
                    && (!protocol.equals(SUPPORTED_PROTOCOL_TLSV1))
                    && (!protocol.equals(SUPPORTED_PROTOCOL_TLSV1_1))
                    && (!protocol.equals(SUPPORTED_PROTOCOL_TLSV1_2))) {
                throw new IllegalArgumentException("protocol " + protocol
                                                   + " is not supported");
            }
        }
        return protocols;
    }

    public static native void SSL_set_cipher_lists(long ssl, String[] ciphers);

    /**
     * Gets the list of cipher suites enabled for the provided {@code SSL} instance.
     *
     * @return array of {@code SSL_CIPHER} references.
     */
    public static native long[] SSL_get_ciphers(long ssl);

    /*
     * Constants for SSL_CIPHER algorithm_mkey (key exchange algorithm).
     * OpenSSL constants from ssl/ssl_locl.h.
     */
    /** RSA key exchange */
    public static final int SSL_kRSA =   0x00000001;
    /** DH cert, RSA CA cert -- no such ciphersuite supported! */
    public static final int SSL_kDHr =   0x00000002;
    /** DH cert, DSA CA cert -- no such ciphersuite supported! */
    public static final int SSL_kDHd =   0x00000004;
    /** tmp DH key no DH cert */
    public static final int SSL_kEDH =   0x00000008;
    /** Kerberos5 key exchange */
    public static final int SSL_kKRB5 =  0x00000010;
    /** ECDH cert, RSA CA cert */
    public static final int SSL_kECDHr = 0x00000020;
    /** ECDH cert, ECDSA CA cert */
    public static final int SSL_kECDHe = 0x00000040;
    /** ephemeral ECDH */
    public static final int SSL_kEECDH = 0x00000080;
    /** PSK */
    public static final int SSL_kPSK =   0x00000100;
    /** GOST key exchange */
    public static final int SSL_kGOST =  0x00000200;
    /** SRP */
    public static final int SSL_kSRP =   0x00000400;

    /*
     * Constants for SSL_CIPHER algorithm_auth (server authentication).
     * OpenSSL constants from ssl/ssl_locl.h.
     */
    /** RSA auth */
    public static final int SSL_aRSA =    0x00000001;
    /** DSS auth */
    public static final int SSL_aDSS =    0x00000002;
    /** no auth (i.e. use ADH or AECDH) */
    public static final int SSL_aNULL =   0x00000004;
    /** Fixed DH auth (kDHd or kDHr) -- no such ciphersuites supported! */
    public static final int SSL_aDH =     0x00000008;
    /** Fixed ECDH auth (kECDHe or kECDHr) */
    public static final int SSL_aECDH =   0x00000010;
    /** KRB5 auth */
    public static final int SSL_aKRB5 =   0x00000020;
    /** ECDSA auth*/
    public static final int SSL_aECDSA =  0x00000040;
    /** PSK auth */
    public static final int SSL_aPSK =    0x00000080;
    /** GOST R 34.10-94 signature auth */
    public static final int SSL_aGOST94 = 0x00000100;
    /** GOST R 34.10-2001 signature auth */
    public static final int SSL_aGOST01 = 0x00000200;

    public static native int get_SSL_CIPHER_algorithm_mkey(long sslCipher);
    public static native int get_SSL_CIPHER_algorithm_auth(long sslCipher);

    public static void setEnabledCipherSuites(long ssl, String[] cipherSuites) {
        checkEnabledCipherSuites(cipherSuites);
        List<String> opensslSuites = new ArrayList<String>();
        for (int i = 0; i < cipherSuites.length; i++) {
            String cipherSuite = cipherSuites[i];
            if (cipherSuite.equals(TLS_EMPTY_RENEGOTIATION_INFO_SCSV)) {
                continue;
            }
            if (cipherSuite.equals(TLS_FALLBACK_SCSV)) {
                SSL_set_mode(ssl, SSL_MODE_SEND_FALLBACK_SCSV);
                continue;
            }
            String openssl = STANDARD_TO_OPENSSL_CIPHER_SUITES.get(cipherSuite);
            String cs = (openssl == null) ? cipherSuite : openssl;
            opensslSuites.add(cs);
        }
        SSL_set_cipher_lists(ssl, opensslSuites.toArray(new String[opensslSuites.size()]));
    }

    public static String[] checkEnabledCipherSuites(String[] cipherSuites) {
        if (cipherSuites == null) {
            throw new IllegalArgumentException("cipherSuites == null");
        }
        // makes sure all suites are valid, throwing on error
        for (int i = 0; i < cipherSuites.length; i++) {
            String cipherSuite = cipherSuites[i];
            if (cipherSuite == null) {
                throw new IllegalArgumentException("cipherSuites[" + i + "] == null");
            }
            if (cipherSuite.equals(TLS_EMPTY_RENEGOTIATION_INFO_SCSV) ||
                    cipherSuite.equals(TLS_FALLBACK_SCSV)) {
                continue;
            }
            if (STANDARD_TO_OPENSSL_CIPHER_SUITES.containsKey(cipherSuite)) {
                continue;
            }
            if (OPENSSL_TO_STANDARD_CIPHER_SUITES.containsKey(cipherSuite)) {
                // TODO log warning about using backward compatability
                continue;
            }
            throw new IllegalArgumentException("cipherSuite " + cipherSuite + " is not supported.");
        }
        return cipherSuites;
    }

    /*
     * See the OpenSSL ssl.h header file for more information.
     */
    public static final int SSL_VERIFY_NONE =                 0x00;
    public static final int SSL_VERIFY_PEER =                 0x01;
    public static final int SSL_VERIFY_FAIL_IF_NO_PEER_CERT = 0x02;

    public static native void SSL_set_accept_state(long sslNativePointer);

    public static native void SSL_set_connect_state(long sslNativePointer);

    public static native void SSL_set_verify(long sslNativePointer, int mode);

    public static native void SSL_set_session(long sslNativePointer, long sslSessionNativePointer)
        throws SSLException;

    public static native void SSL_set_session_creation_enabled(
            long sslNativePointer, boolean creationEnabled) throws SSLException;

    public static native void SSL_set_tlsext_host_name(long sslNativePointer, String hostname)
            throws SSLException;
    public static native String SSL_get_servername(long sslNativePointer);

    /**
     * Enables NPN for all SSL connections in the context.
     *
     * <p>For clients this causes the NPN extension to be included in the
     * ClientHello message.
     *
     * <p>For servers this causes the NPN extension to be included in the
     * ServerHello message. The NPN extension will not be included in the
     * ServerHello response if the client didn't include it in the ClientHello
     * request.
     *
     * <p>In either case the caller should pass a non-null byte array of NPN
     * protocols to {@link #SSL_do_handshake}.
     */
    public static native void SSL_CTX_enable_npn(long sslCtxNativePointer);

    /**
     * Disables NPN for all SSL connections in the context.
     */
    public static native void SSL_CTX_disable_npn(long sslCtxNativePointer);

    /**
     * For clients, sets the list of supported ALPN protocols in wire-format
     * (length-prefixed 8-bit strings).
     */
    public static native int SSL_set_alpn_protos(long sslPointer, byte[] protos);

    /**
     * Returns the selected ALPN protocol. If the server did not select a
     * protocol, {@code null} will be returned.
     */
    public static native byte[] SSL_get0_alpn_selected(long sslPointer);

    /**
     * Returns the sslSessionNativePointer of the negotiated session. If this is
     * a server negotiation, supplying the {@code alpnProtocols} will enable
     * ALPN negotiation.
     */
    public static native long SSL_do_handshake(long sslNativePointer,
                                               FileDescriptor fd,
                                               SSLHandshakeCallbacks shc,
                                               int timeoutMillis,
                                               boolean client_mode,
                                               byte[] npnProtocols,
                                               byte[] alpnProtocols)
        throws SSLException, SocketTimeoutException, CertificateException;

    /**
     * Returns the sslSessionNativePointer of the negotiated session. If this is
     * a server negotiation, supplying the {@code alpnProtocols} will enable
     * ALPN negotiation.
     */
    public static native long SSL_do_handshake_bio(long sslNativePointer,
                                                   long sourceBioRef,
                                                   long sinkBioRef,
                                                   SSLHandshakeCallbacks shc,
                                                   boolean client_mode,
                                                   byte[] npnProtocols,
                                                   byte[] alpnProtocols)
        throws SSLException, SocketTimeoutException, CertificateException;

    public static native byte[] SSL_get_npn_negotiated_protocol(long sslNativePointer);

    /**
     * Currently only intended for forcing renegotiation for testing.
     * Not used within OpenSSLSocketImpl.
     */
    public static native void SSL_renegotiate(long sslNativePointer) throws SSLException;

    /**
     * Returns the local X509 certificate references. Must X509_free when done.
     */
    public static native long[] SSL_get_certificate(long sslNativePointer);

    /**
     * Returns the peer X509 certificate references. Must X509_free when done.
     */
    public static native long[] SSL_get_peer_cert_chain(long sslNativePointer);

    /**
     * Reads with the native SSL_read function from the encrypted data stream
     * @return -1 if error or the end of the stream is reached.
     */
    public static native int SSL_read(long sslNativePointer,
                                      FileDescriptor fd,
                                      SSLHandshakeCallbacks shc,
                                      byte[] b, int off, int len, int readTimeoutMillis)
        throws IOException;

    public static native int SSL_read_BIO(long sslNativePointer,
                                          byte[] dest,
                                          int destOffset,
                                          int destLength,
                                          long sourceBioRef,
                                          long sinkBioRef,
                                          SSLHandshakeCallbacks shc)
        throws IOException;

    /**
     * Writes with the native SSL_write function to the encrypted data stream.
     */
    public static native void SSL_write(long sslNativePointer,
                                        FileDescriptor fd,
                                        SSLHandshakeCallbacks shc,
                                        byte[] b, int off, int len, int writeTimeoutMillis)
        throws IOException;

    public static native int SSL_write_BIO(long sslNativePointer,
                                           byte[] source,
                                           int length,
                                           long sinkBioRef,
                                           SSLHandshakeCallbacks shc)
        throws IOException;

    public static native void SSL_interrupt(long sslNativePointer);
    public static native void SSL_shutdown(long sslNativePointer,
                                           FileDescriptor fd,
                                           SSLHandshakeCallbacks shc) throws IOException;

    public static native void SSL_shutdown_BIO(long sslNativePointer,
                                               long sourceBioRef, long sinkBioRef,
                                               SSLHandshakeCallbacks shc) throws IOException;

    public static native int SSL_get_shutdown(long sslNativePointer);

    public static native void SSL_free(long sslNativePointer);

    public static native byte[] SSL_SESSION_session_id(long sslSessionNativePointer);

    public static native long SSL_SESSION_get_time(long sslSessionNativePointer);

    public static native String SSL_SESSION_get_version(long sslSessionNativePointer);

    public static native String SSL_SESSION_cipher(long sslSessionNativePointer);

    public static native void SSL_SESSION_free(long sslSessionNativePointer);

    public static native byte[] i2d_SSL_SESSION(long sslSessionNativePointer);

    public static native long d2i_SSL_SESSION(byte[] data);

    /**
     * A collection of callbacks from the native OpenSSL code that are
     * related to the SSL handshake initiated by SSL_do_handshake.
     */
    public interface SSLHandshakeCallbacks {
        /**
         * Verify that we trust the certificate chain is trusted.
         *
         * @param sslSessionNativePtr pointer to a reference of the SSL_SESSION
         * @param certificateChainRefs chain of X.509 certificate references
         * @param authMethod auth algorithm name
         *
         * @throws CertificateException if the certificate is untrusted
         */
        public void verifyCertificateChain(long sslSessionNativePtr, long[] certificateChainRefs,
                String authMethod) throws CertificateException;

        /**
         * Called on an SSL client when the server requests (or
         * requires a certificate). The client can respond by using
         * SSL_use_certificate and SSL_use_PrivateKey to set a
         * certificate if has an appropriate one available, similar to
         * how the server provides its certificate.
         *
         * @param keyTypes key types supported by the server,
         * convertible to strings with #keyType
         * @param asn1DerEncodedX500Principals CAs known to the server
         */
        public void clientCertificateRequested(byte[] keyTypes,
                                               byte[][] asn1DerEncodedX500Principals)
            throws CertificateEncodingException, SSLException;

        /**
         * Gets the key to be used in client mode for this connection in Pre-Shared Key (PSK) key
         * exchange.
         *
         * @param identityHint PSK identity hint provided by the server or {@code null} if no hint
         *        provided.
         * @param identity buffer to be populated with PSK identity (NULL-terminated modified UTF-8)
         *        by this method. This identity will be provided to the server.
         * @param key buffer to be populated with key material by this method.
         *
         * @return number of bytes this method stored in the {@code key} buffer or {@code 0} if an
         *         error occurred in which case the handshake will be aborted.
         */
        public int clientPSKKeyRequested(String identityHint, byte[] identity, byte[] key);

        /**
         * Gets the key to be used in server mode for this connection in Pre-Shared Key (PSK) key
         * exchange.
         *
         * @param identityHint PSK identity hint provided by this server to the client or
         *        {@code null} if no hint was provided.
         * @param identity PSK identity provided by the client.
         * @param key buffer to be populated with key material by this method.
         *
         * @return number of bytes this method stored in the {@code key} buffer or {@code 0} if an
         *         error occurred in which case the handshake will be aborted.
         */
        public int serverPSKKeyRequested(String identityHint, String identity, byte[] key);

        /**
         * Called when SSL state changes. This could be handshake completion.
         */
        public void onSSLStateChange(long sslSessionNativePtr, int type, int val);
    }

    // Values used in the SSLHandshakeCallbacks#onSSLStateChange as the {@code type}.
    public static final int SSL_ST_CONNECT = 0x1000;
    public static final int SSL_ST_ACCEPT = 0x2000;
    public static final int SSL_ST_MASK = 0x0FFF;
    public static final int SSL_ST_INIT = (SSL_ST_CONNECT | SSL_ST_ACCEPT);
    public static final int SSL_ST_BEFORE = 0x4000;
    public static final int SSL_ST_OK = 0x03;
    public static final int SSL_ST_RENEGOTIATE = (0x04 | SSL_ST_INIT);

    public static final int SSL_CB_LOOP = 0x01;
    public static final int SSL_CB_EXIT = 0x02;
    public static final int SSL_CB_READ = 0x04;
    public static final int SSL_CB_WRITE = 0x08;
    public static final int SSL_CB_ALERT = 0x4000;
    public static final int SSL_CB_READ_ALERT = (SSL_CB_ALERT | SSL_CB_READ);
    public static final int SSL_CB_WRITE_ALERT = (SSL_CB_ALERT | SSL_CB_WRITE);
    public static final int SSL_CB_ACCEPT_LOOP = (SSL_ST_ACCEPT | SSL_CB_LOOP);
    public static final int SSL_CB_ACCEPT_EXIT = (SSL_ST_ACCEPT | SSL_CB_EXIT);
    public static final int SSL_CB_CONNECT_LOOP = (SSL_ST_CONNECT | SSL_CB_LOOP);
    public static final int SSL_CB_CONNECT_EXIT = (SSL_ST_CONNECT | SSL_CB_EXIT);
    public static final int SSL_CB_HANDSHAKE_START = 0x10;
    public static final int SSL_CB_HANDSHAKE_DONE = 0x20;

    /*
     * From ssl/ssl3.h
     */
    public static final int SSL3_RT_HEADER_LENGTH = 5;
    public static final int SSL_RT_MAX_CIPHER_BLOCK_SIZE = 16;
    public static final int SSL3_RT_MAX_MD_SIZE = 64;
    public static final int SSL3_RT_MAX_PLAIN_LENGTH = 16384;
    public static final int SSL3_RT_MAX_ENCRYPTED_OVERHEAD = 256 + SSL3_RT_MAX_MD_SIZE;
    public static final int SSL3_RT_SEND_MAX_ENCRYPTED_OVERHEAD = SSL_RT_MAX_CIPHER_BLOCK_SIZE
            + SSL3_RT_MAX_MD_SIZE;
    public static final int SSL3_RT_MAX_COMPRESSED_LENGTH = SSL3_RT_MAX_PLAIN_LENGTH;
    public static final int SSL3_RT_MAX_ENCRYPTED_LENGTH = SSL3_RT_MAX_ENCRYPTED_OVERHEAD
            + SSL3_RT_MAX_COMPRESSED_LENGTH;
    public static final int SSL3_RT_MAX_PACKET_SIZE = SSL3_RT_MAX_ENCRYPTED_LENGTH
            + SSL3_RT_HEADER_LENGTH;

    public static native long ERR_peek_last_error();
}

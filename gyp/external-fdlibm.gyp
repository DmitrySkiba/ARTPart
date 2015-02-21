# Copyright (C) 2015 Dmitry Skiba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

{
  'includes': [
    'common.gypi'
  ],

  'variables': {
    'local_root': '<(platform_root)/external/fdlibm',
    'cflags': [
      '-fno-strict-aliasing',

      # TODO only for clang?
      '-Wno-dangling-else',
      '-Wno-logical-op-parentheses',
    ],
  },

  'targets':[
    {
      'target_name': 'external-fdlibm',
      'product_name': 'fdlibm',
      'type': 'static_library',

      'defines': [
        '_IEEE_LIBM',
        '__LITTLE_ENDIAN',
      ],

      'xcode_settings': {
        'OTHER_CFLAGS': [ '<@(cflags)' ]
      },

      'sources': [
        '<(local_root)/k_standard.c',
        '<(local_root)/k_rem_pio2.c',
        '<(local_root)/k_cos.c',
        '<(local_root)/k_sin.c',
        '<(local_root)/k_tan.c',
        '<(local_root)/e_acos.c',
        '<(local_root)/e_acosh.c',
        '<(local_root)/e_asin.c',
        '<(local_root)/e_atan2.c',
        '<(local_root)/e_atanh.c',
        '<(local_root)/e_cosh.c',
        '<(local_root)/e_exp.c',
        '<(local_root)/e_fmod.c',
        '<(local_root)/e_gamma.c',
        '<(local_root)/e_gamma_r.c',
        '<(local_root)/e_hypot.c',
        '<(local_root)/e_j0.c',
        '<(local_root)/e_j1.c',
        '<(local_root)/e_jn.c',
        '<(local_root)/e_lgamma.c',
        '<(local_root)/e_lgamma_r.c',
        '<(local_root)/e_log.c',
        '<(local_root)/e_log10.c',
        '<(local_root)/e_pow.c',
        '<(local_root)/e_rem_pio2.c',
        '<(local_root)/e_remainder.c',
        '<(local_root)/e_scalb.c',
        '<(local_root)/e_sinh.c',
        '<(local_root)/e_sqrt.c',
        '<(local_root)/w_acos.c',
        '<(local_root)/w_acosh.c',
        '<(local_root)/w_asin.c',
        '<(local_root)/w_atan2.c',
        '<(local_root)/w_atanh.c',
        '<(local_root)/w_cosh.c',
        '<(local_root)/w_exp.c',
        '<(local_root)/w_fmod.c',
        '<(local_root)/w_gamma.c',
        '<(local_root)/w_gamma_r.c',
        '<(local_root)/w_hypot.c',
        '<(local_root)/w_j0.c',
        '<(local_root)/w_j1.c',
        '<(local_root)/w_jn.c',
        '<(local_root)/w_lgamma.c',
        '<(local_root)/w_lgamma_r.c',
        '<(local_root)/w_log.c',
        '<(local_root)/w_log10.c',
        '<(local_root)/w_pow.c',
        '<(local_root)/w_remainder.c',
        '<(local_root)/w_scalb.c',
        '<(local_root)/w_sinh.c',
        '<(local_root)/w_sqrt.c',
        '<(local_root)/s_asinh.c',
        '<(local_root)/s_atan.c',
        '<(local_root)/s_cbrt.c',
        '<(local_root)/s_ceil.c',
        '<(local_root)/s_copysign.c',
        '<(local_root)/s_cos.c',
        '<(local_root)/s_erf.c',
        '<(local_root)/s_expm1.c',
        '<(local_root)/s_fabs.c',
        '<(local_root)/s_finite.c',
        '<(local_root)/s_floor.c',
        '<(local_root)/s_frexp.c',
        '<(local_root)/s_ilogb.c',
        '<(local_root)/s_isnan.c',
        '<(local_root)/s_ldexp.c',
        '<(local_root)/s_lib_version.c',
        '<(local_root)/s_log1p.c',
        '<(local_root)/s_logb.c',
        '<(local_root)/s_matherr.c',
        '<(local_root)/s_modf.c',
        '<(local_root)/s_nextafter.c',
        '<(local_root)/s_rint.c',
        '<(local_root)/s_scalbn.c',
        '<(local_root)/s_signgam.c',
        '<(local_root)/s_significand.c',
        '<(local_root)/s_sin.c',
        '<(local_root)/s_tan.c',
        '<(local_root)/s_tanh.c',
      ]
    }
  ]
}
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
  'defines': [
    'U_COMMON_IMPLEMENTATION',
    'ICU_DATA_DIR_PREFIX_ENV_VAR="ANDROID_ROOT"',
    'ICU_DATA_DIR="/usr/icu"',
  ],

  'sources': [
    '<(local_root)/stubdata/stubdata.c',

    '<(local_root)/common/cmemory.c',
    '<(local_root)/common/cstring.c',
    '<(local_root)/common/cwchar.c',
    '<(local_root)/common/locmap.c',
    '<(local_root)/common/punycode.cpp',
    '<(local_root)/common/putil.cpp',
    '<(local_root)/common/uarrsort.c',
    '<(local_root)/common/ubidi.c',
    '<(local_root)/common/ubidiln.c',
    '<(local_root)/common/ubidi_props.c',
    '<(local_root)/common/ubidiwrt.c',
    '<(local_root)/common/ucase.cpp',
    '<(local_root)/common/ucasemap.cpp',
    '<(local_root)/common/ucat.c',
    '<(local_root)/common/uchar.c',
    '<(local_root)/common/ucln_cmn.c',
    '<(local_root)/common/ucmndata.c',
    '<(local_root)/common/ucnv2022.cpp',
    '<(local_root)/common/ucnv_bld.cpp',
    '<(local_root)/common/ucnvbocu.cpp',
    '<(local_root)/common/ucnv.c',
    '<(local_root)/common/ucnv_cb.c',
    '<(local_root)/common/ucnv_cnv.c',
    '<(local_root)/common/ucnvdisp.c',
    '<(local_root)/common/ucnv_err.c',
    '<(local_root)/common/ucnv_ext.cpp',
    '<(local_root)/common/ucnvhz.c',
    '<(local_root)/common/ucnv_io.cpp',
    '<(local_root)/common/ucnvisci.c',
    '<(local_root)/common/ucnvlat1.c',
    '<(local_root)/common/ucnv_lmb.c',
    '<(local_root)/common/ucnvmbcs.c',
    '<(local_root)/common/ucnvscsu.c',
    '<(local_root)/common/ucnv_set.c',
    '<(local_root)/common/ucnv_u16.c',
    '<(local_root)/common/ucnv_u32.c',
    '<(local_root)/common/ucnv_u7.c',
    '<(local_root)/common/ucnv_u8.c',
    '<(local_root)/common/udatamem.c',
    '<(local_root)/common/udataswp.c',
    '<(local_root)/common/uenum.c',
    '<(local_root)/common/uhash.c',
    '<(local_root)/common/uinit.c',
    '<(local_root)/common/uinvchar.c',
    '<(local_root)/common/uloc.cpp',
    '<(local_root)/common/umapfile.c',
    '<(local_root)/common/umath.c',
    '<(local_root)/common/umutex.cpp',
    '<(local_root)/common/unames.cpp',
    '<(local_root)/common/unorm_it.c',
    '<(local_root)/common/uresbund.cpp',
    '<(local_root)/common/ures_cnv.c',
    '<(local_root)/common/uresdata.c',
    '<(local_root)/common/usc_impl.c',
    '<(local_root)/common/uscript.c',
    '<(local_root)/common/uscript_props.cpp',
    '<(local_root)/common/ushape.cpp',
    '<(local_root)/common/ustrcase.cpp',
    '<(local_root)/common/ustr_cnv.c',
    '<(local_root)/common/ustrfmt.c',
    '<(local_root)/common/ustring.cpp',
    '<(local_root)/common/ustrtrns.cpp',
    '<(local_root)/common/ustr_wcs.cpp',
    '<(local_root)/common/utf_impl.c',
    '<(local_root)/common/utrace.c',
    '<(local_root)/common/utrie.cpp',
    '<(local_root)/common/utypes.c',
    '<(local_root)/common/wintz.c',
    '<(local_root)/common/utrie2_builder.cpp',
    '<(local_root)/common/icuplug.c',
    '<(local_root)/common/propsvec.c',
    '<(local_root)/common/ulist.c',
    '<(local_root)/common/uloc_tag.c',
    '<(local_root)/common/ucnv_ct.c',
    '<(local_root)/common/bmpset.cpp',
    '<(local_root)/common/unisetspan.cpp',
    '<(local_root)/common/brkeng.cpp',
    '<(local_root)/common/brkiter.cpp',
    '<(local_root)/common/caniter.cpp',
    '<(local_root)/common/chariter.cpp',
    '<(local_root)/common/dictbe.cpp',
    '<(local_root)/common/locbased.cpp',
    '<(local_root)/common/locid.cpp',
    '<(local_root)/common/locutil.cpp',
    '<(local_root)/common/normlzr.cpp',
    '<(local_root)/common/parsepos.cpp',
    '<(local_root)/common/propname.cpp',
    '<(local_root)/common/rbbi.cpp',
    '<(local_root)/common/rbbidata.cpp',
    '<(local_root)/common/rbbinode.cpp',
    '<(local_root)/common/rbbirb.cpp',
    '<(local_root)/common/rbbiscan.cpp',
    '<(local_root)/common/rbbisetb.cpp',
    '<(local_root)/common/rbbistbl.cpp',
    '<(local_root)/common/rbbitblb.cpp',
    '<(local_root)/common/resbund_cnv.cpp',
    '<(local_root)/common/resbund.cpp',
    '<(local_root)/common/ruleiter.cpp',
    '<(local_root)/common/schriter.cpp',
    '<(local_root)/common/serv.cpp',
    '<(local_root)/common/servlk.cpp',
    '<(local_root)/common/servlkf.cpp',
    '<(local_root)/common/servls.cpp',
    '<(local_root)/common/servnotf.cpp',
    '<(local_root)/common/servrbf.cpp',
    '<(local_root)/common/servslkf.cpp',
    '<(local_root)/common/ubrk.cpp',
    '<(local_root)/common/uchriter.cpp',
    '<(local_root)/common/uhash_us.cpp',
    '<(local_root)/common/uidna.cpp',
    '<(local_root)/common/uiter.cpp',
    '<(local_root)/common/unifilt.cpp',
    '<(local_root)/common/unifunct.cpp',
    '<(local_root)/common/uniset.cpp',
    '<(local_root)/common/uniset_props.cpp',
    '<(local_root)/common/unistr_case.cpp',
    '<(local_root)/common/unistr_cnv.cpp',
    '<(local_root)/common/unistr.cpp',
    '<(local_root)/common/unistr_props.cpp',
    '<(local_root)/common/unormcmp.cpp',
    '<(local_root)/common/unorm.cpp',
    '<(local_root)/common/uobject.cpp',
    '<(local_root)/common/uset.cpp',
    '<(local_root)/common/usetiter.cpp',
    '<(local_root)/common/uset_props.cpp',
    '<(local_root)/common/usprep.cpp',
    '<(local_root)/common/ustack.cpp',
    '<(local_root)/common/ustrenum.cpp',
    '<(local_root)/common/utext.cpp',
    '<(local_root)/common/util.cpp',
    '<(local_root)/common/util_props.cpp',
    '<(local_root)/common/uvector.cpp',
    '<(local_root)/common/uvectr32.cpp',
    '<(local_root)/common/errorcode.cpp',
    '<(local_root)/common/bytestream.cpp',
    '<(local_root)/common/stringpiece.cpp',
    '<(local_root)/common/mutex.cpp',
    '<(local_root)/common/dtintrv.cpp',
    '<(local_root)/common/ucnvsel.cpp',
    '<(local_root)/common/uvectr64.cpp',
    '<(local_root)/common/locavailable.cpp',
    '<(local_root)/common/locdispnames.cpp',
    '<(local_root)/common/loclikely.cpp',
    '<(local_root)/common/locresdata.cpp',
    '<(local_root)/common/normalizer2impl.cpp',
    '<(local_root)/common/normalizer2.cpp',
    '<(local_root)/common/filterednormalizer2.cpp',
    '<(local_root)/common/ucol_swp.cpp',
    '<(local_root)/common/uprops.cpp',
    '<(local_root)/common/utrie2.cpp',
    '<(local_root)/common/charstr.cpp',
    '<(local_root)/common/uts46.cpp',
    '<(local_root)/common/udata.cpp',
    '<(local_root)/common/appendable.cpp',
    '<(local_root)/common/bytestrie.cpp',
    '<(local_root)/common/bytestriebuilder.cpp',
    '<(local_root)/common/bytestrieiterator.cpp',
    '<(local_root)/common/messagepattern.cpp',
    '<(local_root)/common/patternprops.cpp',
    '<(local_root)/common/stringtriebuilder.cpp',
    '<(local_root)/common/ucharstrie.cpp',
    '<(local_root)/common/ucharstriebuilder.cpp',
    '<(local_root)/common/ucharstrieiterator.cpp',
    '<(local_root)/common/dictionarydata.cpp',
    '<(local_root)/common/ustrcase_locale.cpp',
    '<(local_root)/common/unistr_titlecase_brkiter.cpp',
    '<(local_root)/common/uniset_closure.cpp',
    '<(local_root)/common/ucasemap_titlecase_brkiter.cpp',
    '<(local_root)/common/ustr_titlecase_brkiter.cpp',
    '<(local_root)/common/unistr_case_locale.cpp',
  ],
}

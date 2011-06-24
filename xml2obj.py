#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from lxml import etree

def xml2obj(xml, ignore_tag = [], single_tag = [], multi_tag = [], 
            default_single = True):
    '''
    convert xml to python dict
    '''
    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)
    def convert_element(element, ignore_tag=[], single_tag = [], 
                        multi_tag = [], default_single = True, is_root = True):
        children = element.getchildren()
        if element.tag in ignore_tag:
            return etree.tostring(element)
        elif children:
            new_dict = dict()
            for child_elem in children:
                value = convert_element(child_elem, ignore_tag, single_tag,
                                        multi_tag, default_single, False)
                key = _name_mangle(child_elem.tag)
                if new_dict.get(key):
                    if not isinstance(new_dict.get(key,None), list):
                        new_dict[key] = [new_dict[key]]
                    new_dict[key].append(value)
                elif key in multi_tag:
                    new_dict[key] = [value]
                elif key in single_tag:
                    new_dict[key] = value                
                else:
                    if default_single:
                        new_dict[key] = value
                    else:
                        new_dict[key] = [value]
            ret = new_dict
        else:
            ret = element.text and element.text or ''
        #pdb.set_trace()
        if element.attrib:          
            if isinstance(ret, dict):
                ret.update(element.attrib)
            else:
                ret = {'_data':ret}
                ret.update(element.attrib)
        if is_root:
            return {element.tag: ret}
        return ret
    o = etree.fromstring(xml)
    return convert_element(o, ignore_tag, single_tag ,multi_tag,default_single)


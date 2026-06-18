import yaml
import xml.etree.ElementTree as xml_tree

with open('portfolio.yaml', 'r', encoding='utf-8') as file:
    yaml_data = yaml.safe_load(file)

    # 1. Root Element
    feed_element = xml_tree.Element('feed', { 'xmlns': 'http://www.w3.org/2005/Atom' })

    # Prefijo base para links completos (GitHub Pages URL)
    link_prefix = yaml_data['link']

    # 2. METADATA - Root level
    xml_tree.SubElement(feed_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(feed_element, 'subtitle').text = yaml_data['subtitle']
    xml_tree.SubElement(feed_element, 'author').text = yaml_data['author']
    
    # Inyección dinámica del logo de perfil
    if 'logo' in yaml_data:
        xml_tree.SubElement(feed_element, 'logo').text = link_prefix + yaml_data['logo']
    
    # Atributo autovinculado de validación Atom
    xml_tree.SubElement(feed_element, 'link', { 'rel': 'self', 'href': link_prefix + 'portfolio.xml' })

    # 3. Loop para procesar los Items de tu trayectoria
    for item in yaml_data['item']:
        entry_element = xml_tree.SubElement(feed_element, 'entry')
        
        xml_tree.SubElement(entry_element, 'title').text = item['title']
        xml_tree.SubElement(entry_element, 'summary').text = item['description']
        xml_tree.SubElement(entry_element, 'updated').text = item['published']
        
        # --- Link 1: Documentación o Enlace Base ---
        file_url = item['file']
        if file_url.startswith('/'):
            file_url = link_prefix + file_url
            
        xml_tree.SubElement(entry_element, 'link', {
            'rel': 'enclosure',
            'type': item.get('type', 'application/pdf'), 
            'href': file_url
        })
        
        # --- Link 2: Imagen Demostrativa (Preview) ---
        if 'preview_img' in item:
            img_url = item['preview_img']
            if img_url.startswith('/'):
                img_url = link_prefix + img_url
                
            xml_tree.SubElement(entry_element, 'link', {
                'rel': 'enclosure',
                'type': 'image/png',
                'href': img_url
            })

    # 4. Compilación del archivo de salida
    output_tree = xml_tree.ElementTree(feed_element)
    output_tree.write('portfolio.xml', encoding='UTF-8', xml_declaration=True)

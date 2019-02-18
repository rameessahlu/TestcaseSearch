const prettyPrintJson = {
   toHtml: (thing) => {
      const htmlEntities = (string) => {
         // Makes text displayable in browsers
         return string
            .replace(/&/g,   '&amp;')
            .replace(/\\"/g, '&bsol;&quot;')
            .replace(/</g,   '&lt;')
            .replace(/>/g,   '&gt;');
         };
      const replacer = (match, p1, p2, p3, p4) => {
         // Converts the four parenthesized capture groups into HTML
         const part =       { indent: p1, key: p2, value: p3, end: p4 };
         const key =        '<span class=json-key>';
         const val =        '<span class="json-value theme_change '+(univ.theme_toggle?'dark_theme':'')+'">';
         const bool =       '<span class=json-boolean>';
         const str =        '<span class=json-string>';
         const isBool =     ['true', 'false'].includes(part.value);
         const valSpan =    /^"/.test(part.value) ? str : isBool ? bool : val;
         const findName =   /"([\w]+)": |(.*): /;
         const indentHtml = part.indent || '';
         const keyHtml =    part.key ? key + part.key.replace(findName, '$1$2') + '</span>: ' : '';
         const valueHtml =  part.value ? valSpan + part.value + '</span>' : '';
         const endHtml =    part.end || '';
         return indentHtml + keyHtml + valueHtml + endHtml;
         };
      const jsonLine = /^( *)("[^"]+": )?("[^"]*"|[\w.+-]*)?([{}[\],]*)?$/mg;
      return htmlEntities(JSON.stringify(thing, null, 4))
         .replace(jsonLine, replacer);
      }
   };


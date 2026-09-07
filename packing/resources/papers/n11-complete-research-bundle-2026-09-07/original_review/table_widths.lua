function Table(t)
  if #t.colspecs == 3 and #t.head.rows > 0 then
    local first = pandoc.utils.stringify(t.head.rows[1].cells[1].contents)
    local widths = nil
    if first == 'Ref.' then widths = {0.08, 0.44, 0.48}
    elseif first == 'Row' then widths = {0.10, 0.65, 0.25}
    elseif first == 'Priority' then widths = {0.16, 0.42, 0.42}
    elseif first == 'Direction' then widths = {0.20, 0.40, 0.40} end
    if widths then
      for j=1,3 do t.colspecs[j][2] = widths[j] end
    end
  end
  return t
end

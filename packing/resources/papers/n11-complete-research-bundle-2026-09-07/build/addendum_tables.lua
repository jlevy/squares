function Table(t)
  local n = #t.colspecs
  local widths = nil
  if n == 2 then widths = {0.31, 0.69}
  elseif n == 3 then widths = {0.22, 0.39, 0.39} end
  if widths then
    for j = 1,n do t.colspecs[j][2] = widths[j] end
  end
  return t
end

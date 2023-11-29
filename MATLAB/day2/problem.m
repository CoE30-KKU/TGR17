% clear workspace
clc, clearvars, clc

lat_M182 = 15.2235;
long_M182 = 104.8580;

lat_M98 = 15.1334;
long_M98 = 104.7033;

lat = lat_M182;
long = long_M182;

axesm('mercator', 'Grid', 'on', 'MapLatLimit',...
    [lat-10 lat+10], 'MapLonLimit', [long-10 long+10]);

worldmap([lat-10 lat+10], [long-10 long+10]);
load coastlines
geoshow(coastlat, coastlon, 'DisplayType', 'polygon', 'FaceColor', [.45 .60 .30])


plotm(lat, long, 'r*', 'MarkerSize', 10)





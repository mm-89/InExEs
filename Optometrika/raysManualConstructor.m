function rays = raysManualConstructor(position, direction, intensity, wavelength, glass)

%{
    The Rays class constructor doesn't allow to create a bundle of rays
    indicating a specific, independant position, direction and intensity
    for every individual ray, so we need to create an instance of Rays and
    then modify its properties.
    The function should also accept as arguments the same non-geometrical 
    arguments as the Rays class constructor. 
    We must have size(position,1) == size(direction,1) == size(intensity,1)
    == size(wavelength,1)
%}
%{
    INPUT:
    - position  :   an array of 1x3 vector representing the starting position of each ray
    - direction :   (optional) an array of 1x3 vector representing the direction of each ray
                    default : [1 0 0]
    - intensity :   (optional) an array of Double representing the intensity of each ray
                    default : 1 (might be a problem with Lambert sources)
    - wavelength:   (optional) an array of Double representing the wavelength of each ray
                    default : 5300e-10 meters
    - glass     :   (optional) material trough which rays propagate
                    default : 'air'
    
    OUPUT:

    - rays      :   ray bundle object
%}

    % check arguments number
    if nargin == 0 || isempty(position)
        rays = Rays();
        return;
    end
    cnt = size(position,1);
    % check if glass specified
    if nargin < 5 || isempty(glass)
        g = 'air';
    else
        g = glass;
    end
    % check if wavelength specified
    if nargin < 4 || isempty(wavelength)
        w = repmat(5300e-10, cnt, 1);
    elseif size(w,2) ~= 1 || size(w,1) ~= cnt
        error('wavelength must be of dimensions: length of position x 1');
    else
        w = wavelength;
    end
    % check if intesity specified
    if nargin < 3 || isempty(intesity)
        I = repmat(1.0, cnt, 1);
    elseif size(intensity,2) ~= 1 || size(intensity,1) ~= cnt
        error('intensity must be of dimensions: length of position x 1');
    else
        I = intensity;
    end
    % check if direction specified
    if nargin < 2 || isempty(direction)
        n = repmat([1 0 0], cnt, 1);
    elseif size(direction,2) ~= 3 || size(direction,1) ~= cnt
        error('direction must be of dimensions: length of position x 3');
    else
        n = direction;
    end
    
    
    rays        = Rays(cnt, '', '', '', '', '', g, w, '', '');
    rays.cnt    = cnt;
    rays.r      = position;
    rays.n      = n;
    rays.w      = w;
    rays.I      = I;
    rays.nrefr  = refrindx( rays.w, g );
    rays.att    = ones(rays.cnt, 1);
    rays.color  = repmat(rays.color(1,:), cnt,1);
    
end
    
    
    
    
    

function focal = test1()

% testing rays creation possibilities

%{
    Creating a custom pattern for rays bundle.
    Testing raysManualConstructor with custom position
%}

% Creating the positions vector of a concaveLamp using pre-exisiting functions
lens            = Lens( [-40 0 0], 58, 40, -1, {'air' 'bk7'} ); %parabolic surface
rays            = Rays(5000, 'collimated', [-90 0 0], [1 0 0], 100, 'random');
ConcaveLampPos  = rays.intersection(lens).r;

% Creating bundle of rays (direction, intensity and wavelength by default)
ConcaveLamp     = raysManualConstructor(ConcaveLampPos);

% Setting up a bench to draw ConcaveLamp rays
bench = Bench;

% add optical elements in the order they are encountered by light rays

% aperture
aper = Aperture( [ 5 0 0 ], [ 25 80 ] ); % circular aperture
bench.append( aper );

% front lens surface
lens1 = Lens( [ 40 0 0 ], 58, 40, -1, { 'air' 'bk7' } ); % parabolic surface
% back lens surface
lens2 = Lens( [ 60 0 0 ], 58, -70, -3, { 'bk7' 'air' } ); % concave hyperbolic surface
bench.append( { lens1, lens2 } );

% screen
screen = Screen( [ 95 0 0 ], 10, 10, 512, 512 );
bench.append( screen );

% Tracing
rays_through = bench.trace(ConcaveLamp);

% Drawing
bench.draw(rays_through, 'lines');

% Changing others parameters

% Random directions
ConcaveLampN    = ConcaveLamp.copy();
[m n]           = size(ConcaveLampN.n);
ConcaveLamp.n   = rand(m,n);
rays_through    = bench.trace(ConcaveLampN);
bench.draw(rays_through, 'lines');

% Random Intensity
ConcaveLampI    = ConcaveLamp.copy();
ConcaveLampI.I  = rand(m,1);
rays_through    = bench.trace(ConcaveLampI);
bench.draw(rays_through, 'lines');

end


% Hannah Loly - ME 134 Advanced Robotics
% Lab 4 - Kalman
% MATLAB forward kinematics script based on encoder data 

clf; clear all; close all;

sample_time = .1; % seconds
conversion = 3.10*1000; % counts/m for wheel rad 60 mm
A = importdata('raw_data_good.csv');
kalman = importdata('IK_Kalman_good.csv');
kalman_x = kalman(:,1);
kalman_y = kalman(:,2);
pos_left = A(:,1); % left wheel encoder readings 
pos_right = A(:,2); % right wheel encoder readings 
omega_mdps = A(:,4);  % in millidegrees per second
dt = 0.1;  % sampling period in seconds (e.g., 100 Hz sample rate)

% Convert from millidegrees/sec to degrees/sec
omega_dps = omega_mdps / 1000;
d = .16; % track width in [m]

% initialize variables 
theta_deg = zeros(1, length(pos_left)+1);
pos_l_prev = 0;
pos_r_prev = 0;
prev = [0,0]; % x,y position
x_calc = zeros(1, length(pos_left)+1);
y_calc = zeros(1, length(pos_left)+1);
v_l = zeros(1, length(pos_left)+1);
v_r = zeros(1, length(pos_left)+1);

% calculated position
for i = 1:(length(pos_left))
    % use difference between last encoder reading and current 
    v_l(i) = (pos_left(i) - pos_l_prev)/(conversion*sample_time);
    v_r(i) = (pos_right(i) - pos_r_prev)/(conversion*sample_time);
    omega = (v_r(i) - v_l(i))/d; % this is in radians!!! 
    
    if omega~=0 % we are spinning
        R = (d*(v_r(i) + v_l(i)))/(2*(v_r(i) - v_l(i))); 
        % change this to be x_calc(i) instead of prev(1)
        x_calc(i+1) = prev(1) - R*sin(theta_deg(i)) + R*sin(theta_deg(i)+omega*sample_time); 
        y_calc(i+1) = prev(2) + R*cos(theta_deg(i)) - R*cos(theta_deg(i)+omega*sample_time);
        theta_deg(i+1) = theta_deg(i)+omega*sample_time;
    else % just going straight
        velocity = (v_l(i)+v_r(i))/2;
        x_calc(i+1) = prev(1) + velocity*cosd(theta_deg(i))*sample_time;
        y_calc(i+1) = prev(2) + velocity*sind(theta_deg(i))*sample_time;
        theta_deg(i+1) = theta_deg(i);
    end
    prev = [x_calc(i+1), y_calc(i+1)];
    pos_l_prev = pos_left(i);
    pos_r_prev = pos_right(i);
end

figure(1)
hold on
plot(0,0, 'k+', LineWidth=2)
plot(.12, -1.01, 'bo', LineWidth=2)
plot(.522, -1.36, 'b*', LineWidth=2)
plot(.7, -1.14, 'bx', LineWidth=2)
plot(kalman_x/100, kalman_y/100, 'b*')
plot(.14, -.917, 'go', LineWidth=2)
plot(.403, -1.11, 'ro', LineWidth=2)
plot(1.3, -.9, 'r*', LineWidth=2)
plot(.381, -1.16, 'g*',  LineWidth=2)
plot(.4, -1.3, 'rx', LineWidth=2)
plot(.17, -1.17, 'gx', LineWidth=2)


title("Plot of theoretical vs experimental position")
legend("start point", "Kalman", "Theoretical", "Observed", Location="best")
xlabel({'x [m]','Graph is to scale (1:1)'})
ylabel('y [m]')
xlim([-.1,1.4])
ylim([-1.4,.1])
hold off

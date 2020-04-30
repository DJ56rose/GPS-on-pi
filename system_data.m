A = readtable('test_drive_system_data.txt')
B = table2array(A(:,2:3))
for i=1:224
    temperature(i) = B(i,1)
    tempTime(i) = i * 15
end
figure(1)
plot(tempTime,temperature)
title('Temperature of Rapberry Pi CPU vs. Time')
ylabel('Degrees Celsius')
xlabel('Time Since Program Start (s)')
x = 1
y = 0
for i=1:112
    usageOffBeat(i) = B(x,2)
    offBeatTime(i) = y * 30
    x = x + 1
    usageOnBeat(i) = B(x,2)
    onBeatTime(i) = y * 30 + 15
    x = x + 1
    y = y + 1
end
figure(2)
plot(offBeatTime,usageOffBeat)
hold on;
plot(onBeatTime,usageOnBeat)
xlabel('Time Since Program Start (s)')
ylabel('CPU usage (%)')
legend('Off Beat','On Beat')
title('Off beat vs. On beat data gthering affect on CPU usage')
    
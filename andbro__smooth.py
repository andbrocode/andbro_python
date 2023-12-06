def __smooth(y, box_pts):

    from numpy import ones, convolve, hanning

    win = hanning(box_pts)
    y_smooth = convolve(y, win/sum(win), mode='same')

    return y_smooth

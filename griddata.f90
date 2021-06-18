subroutine simple ( ni, nox, noy, sn, xi, yi, zi, xo, yo, zo ) ! {{{

    ! Dimension
    ! ni, length of input data
    ! nox, x length of output data
    ! noy, y length of output data

    ! Input:
    ! sn, number of convolution
    ! xi, input x
    ! yi, input y
    ! zi, input z

    ! Output
    ! xo, output x
    ! yo, output y
    ! zo, output z
    
    implicit none

    integer ( kind = 4 ), intent(in):: ni, nox, noy, sn
    integer ( kind = 4 ) ox, oy, i
    integer ( kind = 4 ) cx, cy, ci

    real ( kind = 8 ), intent(in):: xi(ni), yi(ni), zi(ni)
    real ( kind = 8 ), intent(in):: xo(nox), yo(noy)
    real ( kind = 8 ), intent(out):: zo(nox, noy)
    real ( kind = 8 ) zoc(nox, noy)
    real ( kind = 8 ) zn(nox, noy), cn, cz
    real ( kind = 8 ) dx, dy
    integer (kind = 4) znan_xi(nox*noy), znan_yi(nox*noy), n_nan, n1_nan
    dx = xo(2)-xo(1)
    dy = yo(2)-yo(1)
    zo(:,:) = 0
    zn(:,:) = 0

    do i = 1, ni
        if (xi(i) .ge. xo(1) .and. xi(i) .le. xo(nox)+dx .and. &
            yi(i) .ge. yo(1) .and. yi(i) .le. yo(noy)+dy) then  
            ox = floor((xi(i)-xo(1))/dx)+1
            if (ox .gt. nox) then 
                ox = nox
            endif
            oy = floor((yi(i)-yo(1))/dy)+1
            if (oy .gt. noy) then
                oy = noy
            endif
            zn(ox, oy) = zn(ox, oy)+1; 
            zo(ox, oy) = zo(ox, oy)+zi(i); 
        endif
    enddo
  
    n_nan = 0
    do oy = 1, noy
        do ox = 1, nox
            if (zn(ox, oy) .eq. 0) then
                zo(ox, oy) = -999; 
                n_nan = n_nan+1 
                znan_xi(n_nan) = ox 
                znan_yi(n_nan) = oy 
            else
                zo(ox, oy) = zo(ox, oy)/zn(ox, oy)
            endif
        enddo
    enddo

    do ci = 1, sn
        if (n_nan .ge. 1) then
            write(*,*)ci
            zoc = zo
            n1_nan = 0
            do i = 1, n_nan
                ox = znan_xi(i)
                oy = znan_yi(i)
                if (zo(ox, oy) .lt. -990) then
                    cn = 0
                    cz = 0
                    do cy = -1, 1
                        do cx = -1, 1 
                            if (ox+cx .le. nox .and. ox+cx .ge. 1 .and. &
                                oy+cy .le. noy .and. oy+cy .ge. 1) then
                                if (zo(ox+cx, oy+cy) .gt. -990) then 
                                    cn = cn+1
                                    cz = cz+zo(ox+cx, oy+cy)
                                endif
                            endif
                        enddo
                    enddo
                    if (cn .gt. 0) then
                        zoc(ox, oy) = cz/cn
                    else  
                        n1_nan = n1_nan+1
                        znan_xi(n1_nan) = ox
                        znan_yi(n1_nan) = oy
                    endif 
                endif
            enddo
            n_nan = n1_nan
            zo = zoc
        endif
    enddo

    write(*,*)'end griddata'
    return
end subroutine simple ! }}}

subroutine pbp ( nix, niy, nox, noy, xi, yi, zi, xo, yo, zo ) !{{{
    implicit none

    integer (kind = 8), intent (in):: nix, niy, nox, noy
    integer (kind = 8) ox, oy, ix, iy !, ix0, iy0
    integer (kind = 8) next_out  ! cx, cy, ci
    integer (kind = 8) w, dr, n, md, i, k ! , j, m

    real (kind = 8), intent (in):: xi(nix, niy), yi(nix, niy), zi(nix, niy)
    real (kind = 8), intent (in):: xo(nox), yo(noy)
    real (kind = 8), intent (out):: zo(nox, noy)
    ! real (kind = 8) zn(nox, noy), cn, cz
    real (kind = 8) a1, b1, c1, d1, a2, b2, c2, d2
    ! real (kind = 8) dx, dy, a1, b1, c1, d1, a2, b2, c2, d2
    real (kind = 8) x1, x2, x3, x4, y1, y2, y3, y4, z1, z2, z3, z4, px, py, x13, x24, y12, y34, y32, y14
    real (kind = 8) z(4), ds(4), wf(4), zup, zdown, d12, d34, d13, d24, s12, s34, s13, s24

    zo(:,:) = 0 
    !do ix = 1, nox
    !    do iy = 1, noy
    !        zo(ix, iy) = 0
    !    enddo
    !enddo

    write(*,*)'t5'
    if (.true.) then
    ix = 1
    iy = 1
    do iy = 1, niy-1
        do ix = 1, nix-1
            ! write(*,*)ix, iy, xi(ix, iy), yi(ix, iy)
            if (xi(ix, iy) >= -180 .and. yi(ix, iy) >= -90 .and. &
                xi(ix+1, iy) >= -180 .and. yi(ix+1, iy) >= -90 .and. &
                xi(ix, iy+1) >= -180 .and. yi(ix, iy+1) >= -90 .and. &
                xi(ix+1, iy+1) >= -180 .and. yi(ix+1, iy+1) >= -90 ) then
                goto 100
            endif
        enddo
    enddo

100 oy = 1
    write(*,*)'finish step 1'
    ! write(*,*)ix, iy
    ix = 1000 
    iy = 1000
    ox = 1
    dr = 1
    n = 1 
    w = 1
    md = 0
    do while (w .gt. 0)
        px = xo(ox)
        py = yo(oy)
        x1 = xi(ix, iy)
        x2 = xi(ix+1, iy)
        x3 = xi(ix, iy+1)
        x4 = xi(ix+1, iy+1)
        y1 = yi(ix, iy)
        y2 = yi(ix+1, iy)
        y3 = yi(ix, iy+1)
        y4 = yi(ix+1, iy+1)
        z1 = zi(ix, iy)
        z2 = zi(ix+1, iy)
        z3 = zi(ix, iy+1)
        z4 = zi(ix+1, iy+1)
        x13 = x1-(y1-py)/(y1-y3)*(x1-x3)
        x24 = x2-(y2-py)/(y2-y4)*(x2-x4)
        y12 = y1-(x1-px)/(x1-x2)*(y1-y2)
        y34 = y3-(x3-px)/(x3-x4)*(y3-y4)
        n = n+1

        if (px .le. x24 .and. px .ge. x13 .and. py .le. y34 .and. py .ge. y12) then
            ds(1) = sqrt((px-x1)**2+(py-y1)**2)
            ds(2) = sqrt((px-x2)**2+(py-y2)**2)
            ds(3) = sqrt((px-x3)**2+(py-y3)**2)
            ds(4) = sqrt((px-x4)**2+(py-y4)**2)
            k = 0
            do i = 1, 4
                wf(i) = 0
                if (ds(i) .eq. 0) k = i 
            enddo
            if (k .gt. 0) then
                wf(k) = 1
            else 
                wf = 1/ds/(sum(1/ds))
            endif
           
            zo(ox, oy) = sum(z*wf)
            s12 = sqrt((x2-x1)**2+(y2-y1)**2)
            s34 = sqrt((x3-x4)**2+(y3-y4)**2)
            s13 = sqrt((x1-x3)**2+(y1-y3)**2)
            s24 = sqrt((x2-x4)**2+(y2-y4)**2)

            d13 = ds(1)+ds(3)-s13
            d12 = ds(1)+ds(2)-s12
            d34 = ds(3)+ds(4)-s34
            d24 = ds(2)+ds(4)-s24

            zup = z(3)*d24/(d13+d24)+z(4)*d13/(d13+d24)
            zdown = z(1)*d24/(d13+d24)+z(2)*d13/(d13+d24)
            zo(ox, oy) = zup*d12/(d12+d34)+zdown*d34/(d12+d34)

            if (.true.) then
                a1 = y1*z2-y1*z3-y2*z1+y2*z3+y3*z1-y3*z2
                b1 = -x1*z2+x1*z3+x2*z1-x2*z3-x3*z1+x3*z2
                c1 = x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2
                d1 = -x1*y2*z3+x1*y3*z2+x2*y1*z3-x2*y3*z1-x3*y1*z2+x3*y2*z1
                a2 = y4*z2-y4*z3-y2*z4+y2*z3+y3*z4-y3*z2
                b2 = -x4*z2+x4*z3+x2*z4-x2*z3-x3*z4+x3*z2
                c2 = x4*y2-x4*y3-x2*y4+x2*y3+x3*y4-x3*y2
                d2 = -x4*y2*z3+x4*y3*z2+x2*y4*z3-x2*y3*z4-x3*y4*z2+x3*y2*z4
                y32 = y3-(x3-px)/(x3-x2)*(y3-y2)
                if (py < y32) then
                    zo(ox, oy) = (-d1-a1*px-b1*py)/c1
                else
                    zo(ox, oy) = (-d2-a2*px-b2*py)/c2
                endif 
            else
                a1 = y1*z4-y1*z3-y4*z1+y4*z3+y3*z1-y3*z4
                b1 = -x1*z4+x1*z3+x4*z1-x4*z3-x3*z1+x3*z4
                c1 = x1*y4-x1*y3-x4*y1+x4*y3+x3*y1-x3*y4
                d1 = -x1*y4*z3+x1*y3*z4+x4*y1*z3-x4*y3*z1-x3*y1*z4+x3*y4*z1
                a2 = y4*z2-y4*z1-y2*z4+y2*z1+y1*z4-y1*z2
                b2 = -x4*z2+x4*z1+x2*z4-x2*z1-x1*z4+x1*z2
                c2 = x4*y2-x4*y1-x2*y4+x2*y1+x1*y4-x1*y2
                d2 = -x4*y2*z1+x4*y1*z2+x2*y4*z1-x2*y1*z4-x1*y4*z2+x1*y2*z4
                y14 = y1-(x1-px)/(x1-x4)*(y1-y4)
                if (py > y14) then
                    zo(ox, oy) = (-d1-a1*px-b1*py)/c1
                else
                    zo(ox, oy) = (-d2-a2*px-b2*py)/c2
                endif 
            endif

            if (ox .eq. nox .and. dr .eq. 1) then
                dr = -1
                oy = oy+1
                md = 1
            endif
            if (ox .eq. 1 .and. dr .eq. -1) then
                dr = 1
                if (oy .gt. 1) then
                    oy = oy+1
                    md = 1
                endif
            endif
            if (ox .lt. nox .and. dr .eq. 1 .and. md .eq. 0) then
                ox = ox+1
            endif
            if (ox .gt. 1 .and. dr .eq. -1 .and. md .eq. 0) then
                ox = ox-1
            endif
            md = 0
        endif
        if (oy .gt. noy) then
            w = 0
        endif 

        if (px .gt. x24) then
            ix = ix+1
        endif
        if (px .lt. x13) then
            ix = ix-1
        endif
        if (py .gt. y34) then
            iy = iy+1
        endif
        if (py .lt. y12) then
            iy = iy-1
        endif

        next_out = 0 
        if (ix <= 0) then 
            ix = 1
            next_out = 1
        endif 
        if (ix > nix-1) then 
            ix = nix-1
            next_out = 1
        endif 
        if (iy <= 0) then 
            iy = 1
            next_out = 1
        endif 
        if (iy > niy-1) then 
            iy = niy-1
            next_out = 1
        endif 
        
        if (xi(ix, iy) < -200 .or. yi(ix, iy) < -200 .or. &
            xi(ix+1, iy) < -200 .or. yi(ix+1, iy) < -200 .or. &
            xi(ix, iy+1) < -200 .or. yi(ix, iy+1) < -200 .or. &
            xi(ix+1, iy+1) < -200 .or. yi(ix+1, iy+1) < -200 ) then
            next_out = 1
        endif 

        if (next_out == 1) then
            if (ox .eq. nox .and. dr .eq. 1) then
                dr = -1
                oy = oy+1
                md = 1
            endif
            if (ox .eq. 1 .and. dr .eq. -1) then
                dr = 1
                if (oy .gt. 1) then
                    oy = oy+1
                    md = 1
                endif
            endif
            if (ox .lt. nox .and. dr .eq. 1 .and. md .eq. 0) then
                ox = ox+1
            endif
            if (ox .gt. 1 .and. dr .eq. -1 .and. md .eq. 0) then
                ox = ox-1
            endif
            md = 0
        endif
    enddo 

    endif
    write(*,*)'end griddata'
    return
end subroutine pbp !}}}

subroutine stb ( nix, niy, nox, noy, sn, xi, yi, zi, xo, yo, zo ) ! {{{
    implicit none

    integer (kind = 8), intent(in):: nix, niy, nox, noy, sn
    integer (kind = 8) zox(nox, noy), zoy(nox, noy)
    integer (kind = 8) zoxc(nox, noy), zoyc(nox, noy)
    integer (kind = 8) ox, oy, ix, iy
    integer (kind = 8) w, n
    integer (kind = 8) znan_xi(nox*noy), znan_yi(nox*noy), n_nan, n1_nan
    integer (kind = 8 ) i
    integer (kind = 8 ) cx, cy, ci

    real (kind = 8), intent(in):: xi(nix, niy), yi(nix, niy), zi(nix, niy)
    real (kind = 8), intent(in):: xo(nox), yo(noy)
    real (kind = 8), intent(out):: zo(nox, noy)
    real (kind = 8) dx, dy, a1, b1, c1, d1, a2, b2, c2, d2
    real (kind = 8) x1, x2, x3, x4, y1, y2, y3, y4, z1, z2, z3, z4, px, py, x13, x24, y12, y34, y32
    real ( kind = 8 ) cn  ! zn(nox, noy), cn, cz

    ! generate the preliminary input position for output grids
    ! {{{
    dx = xo(2)-xo(1)
    dy = yo(2)-yo(1)
    zox(:,:) = -9
    zoy(:,:) = -9
    do iy = 1, niy
        do ix = 1, nix
            if (xi(ix, iy) .ge. xo(1) .and. xi(ix, iy) .le. xo(nox)+dx .and. &
                yi(ix, iy) .ge. yo(1) .and. yi(ix, iy) .le. yo(noy)+dy) then  
                ox = floor((xi(ix, iy)-xo(1))/dx)+1
                oy = floor((yi(ix, iy)-yo(1))/dy)+1
                if (ox .ge. 1 .and. ox .le. nox .and. oy .ge. 1 .and. oy .le. noy) then
                    if (zox(ox, oy) .le. 0) then 
                        zox(ox, oy) = ix; 
                        zoy(ox, oy) = iy; 
                    endif
                endif
            endif
        enddo
    enddo
    ! }}}

    ! complete the inner output grids
    if (.true.) then
    n_nan = 0
    do oy = 1, noy
        do ox = 1, nox
            if (zox(ox, oy) .lt. 1) then
                n_nan = n_nan+1 
                znan_xi(n_nan) = ox 
                znan_yi(n_nan) = oy 
            endif
        enddo
    enddo
    write(*,*)'n_nan',n_nan
    do ci = 1, sn ! {{{
        if (n_nan .ge. 1) then
            write(*,*)ci
            n1_nan = 0
            zoxc = zox
            zoyc = zoy
            do i = 1, n_nan
                ox = znan_xi(i)
                oy = znan_yi(i)
                !write(*,*)'ox, oy',ox, oy
                if (zox(ox, oy) .lt. -8) then
                    cn = 0
                    do cy = -1, 1
                        do cx = -1, 1 
                            if (ox+cx .le. nox .and. ox+cx .ge. 1 .and. &
                                oy+cy .le. noy .and. oy+cy .ge. 1) then
                                !write(*,*)'ox+cx, oy+cy',ox+cx, oy+cy
                                if (zox(ox+cx, oy+cy) .gt. -8) then
                                    cn = cn+1
                                    zoxc(ox, oy) = zox(ox+cx, oy+cy); 
                                    zoyc(ox, oy) = zoy(ox+cx, oy+cy); 
                                    goto 300
                                endif
                            endif
                        enddo
                    enddo
                    300 continue
                    if (cn .le. 0) then
                        !write(*,*)'n1_nan, ',n1_nan
                        n1_nan = n1_nan+1
                        znan_xi(n1_nan) = ox
                        znan_yi(n1_nan) = oy
                    endif 
                endif
            enddo
            n_nan = n1_nan
            zox = zoxc
            zoy = zoyc
        endif
    enddo ! }}}
    endif

    ! Interplate
    ! {{{
    write(*,*)'int'
    do oy = 1, noy
        do ox = 1, nox
            w = 1
            ix = zox(ox, oy)
            iy = zoy(ox, oy)
            !write(*,*)ox, oy
            !write(*,*)ox, oy
            !write(*,*)'ix, iy'
            !write(*,*)ix, iy
            n = 0
            do while (w > 0 .and. n < 10 .and. ix > 1 .and. iy > 1 .and. ix <= nix .and. iy <= niy)
                n = n+1
                px = xo(ox)
                py = yo(oy)

                !write(*,*)ix, iy
                x1 = xi(ix-1, iy-1)
                x2 = xi(ix, iy-1)
                x3 = xi(ix-1, iy)
                x4 = xi(ix, iy)
                y1 = yi(ix-1, iy-1)
                y2 = yi(ix, iy-1)
                y3 = yi(ix-1, iy)
                y4 = yi(ix, iy)
                if (x1 < -180 .or. x2 < -180 .or. x3 < -180 .or. x4 < -180 .or. &
                    y1 < -90  .or. y2 < -90  .or. y3 < -90  .or. y4 < -90) then 
                    w = 0
                    goto 200
                endif 
                z1 = zi(ix-1, iy-1)
                z2 = zi(ix, iy-1)
                z3 = zi(ix-1, iy)
                z4 = zi(ix, iy)

                x13 = x1-(y1-py)/(y1-y3)*(x1-x3)
                x24 = x2-(y2-py)/(y2-y4)*(x2-x4)
                y12 = y1-(x1-px)/(x1-x2)*(y1-y2)
                y34 = y3-(x3-px)/(x3-x4)*(y3-y4)

                if (px .le. x24 .and. px .ge. x13 .and. py .le. y34 .and. py .ge. y12) then
                    a1 = y1*z2-y1*z3-y2*z1+y2*z3+y3*z1-y3*z2
                    b1 = -x1*z2+x1*z3+x2*z1-x2*z3-x3*z1+x3*z2
                    c1 = x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2
                    d1 = -x1*y2*z3+x1*y3*z2+x2*y1*z3-x2*y3*z1-x3*y1*z2+x3*y2*z1
                    a2 = y4*z2-y4*z3-y2*z4+y2*z3+y3*z4-y3*z2
                    b2 = -x4*z2+x4*z3+x2*z4-x2*z3-x3*z4+x3*z2
                    c2 = x4*y2-x4*y3-x2*y4+x2*y3+x3*y4-x3*y2
                    d2 = -x4*y2*z3+x4*y3*z2+x2*y4*z3-x2*y3*z4-x3*y4*z2+x3*y2*z4
                    y32 = y3-(x3-px)/(x3-x2)*(y3-y2)
                    if (py < y32) then
                        zo(ox, oy) = (-d1-a1*px-b1*py)/c1
                    else
                        zo(ox, oy) = (-d2-a2*px-b2*py)/c2
                    endif 
                    w = 0
                else
                    !write(*,*)'change, i'
                    if (px .gt. x24) then
                        ix = ix+1
                    endif
                    if (px .lt. x13) then
                        ix = ix-1
                    endif
                    if (py .gt. y34) then
                        iy = iy+1
                    endif
                    if (py .lt. y12) then
                        iy = iy-1
                    endif
                endif
                200 continue
            enddo
        enddo
    enddo 
    ! }}}

    write(*,*)'end griddata'
    return
end subroutine stb ! }}}

subroutine most ( ni, nox, noy, sn, xi, yi, zi, xo, yo, zo ) ! {{{

    ! Dimension
    ! ni, length of input data
    ! nox, x length of output data
    ! noy, y length of output data

    ! Input:
    ! sn, number of convolution
    ! xi, input x
    ! yi, input y
    ! zi, input z

    ! Output
    ! xo, output x
    ! yo, output y
    ! zo, output z
    
    implicit none

    integer ( kind = 4 ), intent(in):: ni, nox, noy, sn
    integer ( kind = 4 ) ox, oy, i
    integer ( kind = 4 ) cx, cy, ci

    real ( kind = 8 ), intent(in):: xi(ni), yi(ni), zi(ni)
    real ( kind = 8 ), intent(in):: xo(nox), yo(noy)
    real ( kind = 8 ), intent(out):: zo(nox, noy)
    real ( kind = 8 ) zoc(nox, noy)
    real ( kind = 8 ) zn(nox, noy), cn, cz
    real ( kind = 8 ) dx, dy
    integer (kind = 4) znan_xi(nox*noy), znan_yi(nox*noy), n_nan, n1_nan
    dx = xo(2)-xo(1)
    dy = yo(2)-yo(1)
    zo(:,:) = 0
    zn(:,:) = 0

    do i = 1, ni
        if (xi(i) .ge. xo(1) .and. xi(i) .le. xo(nox)+dx .and. &
            yi(i) .ge. yo(1) .and. yi(i) .le. yo(noy)+dy) then  
            ox = floor((xi(i)-xo(1))/dx)+1
            if (ox .gt. nox) then 
                ox = nox
            endif
            oy = floor((yi(i)-yo(1))/dy)+1
            if (oy .gt. noy) then
                oy = noy
            endif
            zn(ox, oy) = zn(ox, oy)+1; 
            zo(ox, oy) = zo(ox, oy)+zi(i); 
        endif
    enddo
  
    n_nan = 0
    do oy = 1, noy
        do ox = 1, nox
            if (zn(ox, oy) .eq. 0) then
                zo(ox, oy) = -999; 
                n_nan = n_nan+1 
                znan_xi(n_nan) = ox 
                znan_yi(n_nan) = oy 
            else
                zo(ox, oy) = zo(ox, oy)/zn(ox, oy)
            endif
        enddo
    enddo

    do ci = 1, sn
        if (n_nan .ge. 1) then
            write(*,*)ci
            zoc = zo
            n1_nan = 0
            do i = 1, n_nan
                ox = znan_xi(i)
                oy = znan_yi(i)
                if (zo(ox, oy) .lt. -990) then
                    cn = 0
                    cz = 0
                    do cy = -1, 1
                        do cx = -1, 1 
                            if (ox+cx .le. nox .and. ox+cx .ge. 1 .and. &
                                oy+cy .le. noy .and. oy+cy .ge. 1) then
                                if (zo(ox+cx, oy+cy) .gt. 0) then 
                                    cn = cn+1
                                    zoc(ox, oy) = zo(ox+cx, oy+cy)  ! test 
                                endif
                            endif
                        enddo
                    enddo
                    if (cn .gt. 0) then
                        continue
                    else  
                        n1_nan = n1_nan+1
                        znan_xi(n1_nan) = ox
                        znan_yi(n1_nan) = oy
                    endif 
                endif
            enddo
            n_nan = n1_nan
            zo = zoc
        endif
    enddo

    write(*,*)'end griddata'
    return
end subroutine most ! }}}


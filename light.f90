subroutine simple ( nx, ny, x, y, z, l, r) ! {{{

    ! Dimension
    ! nx, x length of output data
    ! ny, y length of output data

    ! Input:
    ! x, input x
    ! y, input y
    ! z, input z

    ! Output
    ! l, output lighting
    
    implicit none

    integer ( kind = 4 ), intent(in):: nx, ny

    real ( kind = 8 ), intent(in):: x(nx, ny), y(nx, ny), z(nx, ny), l(3)
    real ( kind = 8 ), intent(out):: r(nx, ny)
    
    integer ( kind = 4 ) ix, iy
    real ( kind = 8 )  x1, x2, y1, y2, z1, z2, xn, yn, zn, xr, yr, zr, m

    do iy = 1, ny-1
        do ix = 1, nx-1
            x1 = x(ix, iy+1)-x(ix, iy)
            y1 = y(ix, iy+1)-y(ix, iy)
            z1 = z(ix, iy+1)-z(ix, iy)

            x2 = x(ix+1, iy)-x(ix, iy)
            y2 = y(ix+1, iy)-y(ix, iy)
            z2 = z(ix+1, iy)-z(ix, iy)

            xn = y1*z2-y2*z1
            yn = z1*x2-z2*x1
            zn = x1*y2-x2*y1
            m = sqrt(xn**2+yn**2+zn**2)
            xn = xn/m
            yn = yn/m
            zn = zn/m

            xr = l(1)
            yr = l(2)
            zr = l(3)
            m = sqrt(xr**2+yr**2+zr**2)
            xr = xr/m
            yr = yr/m
            zr = zr/m

            r(ix, iy) = xr*xn+yr*yn+zr*zn

        enddo
        r(nx, iy) = r(nx-1, iy)
    enddo
    do ix = 1, nx
        r(ix, ny) = r(ix, ny-1)
    enddo

end subroutine simple ! }}}
   
subroutine point ( nx, ny, x, y, z, l, r) ! {{{

    ! Dimension
    ! nx, x length of output data
    ! ny, y length of output data

    ! Input:
    ! x, input x
    ! y, input y
    ! z, input z

    ! Output
    ! l, output lighting (normal in each point)
    
    implicit none

    integer ( kind = 4 ), intent(in):: nx, ny
    real ( kind = 8 ), intent(in):: x(nx, ny), y(nx, ny), z(nx, ny), l(3)
    real ( kind = 8 ), intent(out):: r(nx, ny)
    
    integer ( kind = 4 ) ix, iy, iq
    real ( kind = 8 )  x1, x2, y1, y2, z1, z2, xn, yn, zn, xr, yr, zr, m

    do iy = 1, ny-1
        do ix = 1, nx-1
            r(ix, iy) = 0
            do iq = 1, 4
                if (iq .eq. 1) then
                    x1 = x(ix, iy+1)-x(ix, iy)
                    y1 = y(ix, iy+1)-y(ix, iy)
                    z1 = z(ix, iy+1)-z(ix, iy)
                    x2 = x(ix+1, iy)-x(ix, iy)
                    y2 = y(ix+1, iy)-y(ix, iy)
                    z2 = z(ix+1, iy)-z(ix, iy)
                endif
                if (iq .eq. 2) then
                    x1 = x(ix+1, iy)-x(ix, iy)
                    y1 = y(ix+1, iy)-y(ix, iy)
                    z1 = z(ix+1, iy)-z(ix, iy)
                    x2 = x(ix, iy-1)-x(ix, iy)
                    y2 = y(ix, iy-1)-y(ix, iy)
                    z2 = z(ix, iy-1)-z(ix, iy)
                endif
                if (iq .eq. 3) then
                    x1 = x(ix, iy-1)-x(ix, iy)
                    y1 = y(ix, iy-1)-y(ix, iy)
                    z1 = z(ix, iy-1)-z(ix, iy)
                    x2 = x(ix-1, iy)-x(ix, iy)
                    y2 = y(ix-1, iy)-y(ix, iy)
                    z2 = z(ix-1, iy)-z(ix, iy)
                endif
                if (iq .eq. 4) then
                    x1 = x(ix-1, iy)-x(ix, iy)
                    y1 = y(ix-1, iy)-y(ix, iy)
                    z1 = z(ix-1, iy)-z(ix, iy)
                    x2 = x(ix, iy+1)-x(ix, iy)
                    y2 = y(ix, iy+1)-y(ix, iy)
                    z2 = z(ix, iy+1)-z(ix, iy)
                endif

                xn = y1*z2-y2*z1
                yn = z1*x2-z2*x1
                zn = x1*y2-x2*y1
                m = sqrt(xn**2+yn**2+zn**2)
                xn = xn/m
                yn = yn/m
                zn = zn/m

                xr = l(1)
                yr = l(2)
                zr = l(3)
                m = sqrt(xr**2+yr**2+zr**2)
                xr = xr/m
                yr = yr/m
                zr = zr/m

                r(ix, iy) = r(ix, iy)+xr*xn+yr*yn+zr*zn
            enddo
            r(ix, iy) = r(ix, iy)/4
        enddo
        r(nx, iy) = r(nx-1, iy)
    enddo
    do ix = 1, nx
        r(ix, ny) = r(ix, ny-1)
    enddo

end subroutine point ! }}}


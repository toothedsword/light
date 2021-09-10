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

    real ( kind = 8 ), intent(in):: x(ny, nx), y(ny, nx), z(ny, nx), l(3)
    real ( kind = 8 ), intent(out):: r(ny, nx)
    
    integer ( kind = 4 ) ix, iy
    real ( kind = 8 )  x1, x2, y1, y2, z1, z2, xn, yn, zn, xr, yr, zr, m

    do ix = 1, nx-1
        do iy = 1, ny-1
            x1 = x(iy, ix+1)-x(iy, ix)
            y1 = y(iy, ix+1)-y(iy, ix)
            z1 = z(iy, ix+1)-z(iy, ix)

            x2 = x(iy+1, ix)-x(iy, ix)
            y2 = y(iy+1, ix)-y(iy, ix)
            z2 = z(iy+1, ix)-z(iy, ix)

            xn = y1*z2-y2*z1
            yn = z1*x2-z2*x1
            zn = x1*y2-x2*y1
            ! write(*,*)x1*y2, x2*y1, x1*y2-x2*y1
            m = sqrt(xn**2+yn**2+zn**2)
            xn = xn/m
            yn = yn/m
            ! zn = zn/m

            xr = l(1)
            yr = l(2)
            zr = l(3)
            m = sqrt(xr**2+yr**2+zr**2)
            xr = xr/m
            yr = yr/m
            zr = zr/m

            r(iy, ix) = zn  ! xr*xn+yr*yn+zr*zn

        enddo
        r(ny, ix) = r(ny-1, ix)
    enddo
    do iy = 1, ny
        r(iy, nx) = r(iy, nx-1)
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
    ! l, light position

    ! Output
    ! r, output lighting (normal_in_each_point x l)
    implicit none

    integer ( kind = 4 ), intent(in):: nx, ny
    real ( kind = 8 ), intent(in):: x(ny, nx), y(ny, nx), z(ny, nx), l(3)
    real ( kind = 8 ), intent(out):: r(ny, nx)
    
    integer ( kind = 4 ) ix, iy, iq
    real ( kind = 8 )  x1, x2, y1, y2, z1, z2, xn, yn, zn, xr, yr, zr, m, rn, ri

    do ix = 1, nx
        do iy = 1, ny
            r(iy, ix) = 0
            rn = 0
            do iq = 1, 4
                ri = 0
                if (iq .eq. 1 .and. ix < nx .and. iy < ny) then
                    x1 = x(iy, ix+1)-x(iy, ix)
                    y1 = y(iy, ix+1)-y(iy, ix)
                    z1 = z(iy, ix+1)-z(iy, ix)
                    x2 = x(iy+1, ix)-x(iy, ix)
                    y2 = y(iy+1, ix)-y(iy, ix)
                    z2 = z(iy+1, ix)-z(iy, ix)
                    ri = 1
                endif
                if (iq .eq. 2 .and. ix > 1 .and. iy < ny) then
                    x1 = x(iy+1, ix)-x(iy, ix)
                    y1 = y(iy+1, ix)-y(iy, ix)
                    z1 = z(iy+1, ix)-z(iy, ix)
                    x2 = x(iy, ix-1)-x(iy, ix)
                    y2 = y(iy, ix-1)-y(iy, ix)
                    z2 = z(iy, ix-1)-z(iy, ix)
                    ri = 1
                endif
                if (iq .eq. 3 .and. ix > 1 .and. iy > 1) then
                    x1 = x(iy, ix-1)-x(iy, ix)
                    y1 = y(iy, ix-1)-y(iy, ix)
                    z1 = z(iy, ix-1)-z(iy, ix)
                    x2 = x(iy-1, ix)-x(iy, ix)
                    y2 = y(iy-1, ix)-y(iy, ix)
                    z2 = z(iy-1, ix)-z(iy, ix)
                    ri = 1
                endif
                if (iq .eq. 4 .and. ix < nx .and. iy > 1) then
                    x1 = x(iy-1, ix)-x(iy, ix)
                    y1 = y(iy-1, ix)-y(iy, ix)
                    z1 = z(iy-1, ix)-z(iy, ix)
                    x2 = x(iy, ix+1)-x(iy, ix)
                    y2 = y(iy, ix+1)-y(iy, ix)
                    z2 = z(iy, ix+1)-z(iy, ix)
                    ri = 1
                endif

                if (ri > 0) then
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
                    r(iy, ix) = r(iy, ix)+xr*xn+yr*yn+zr*zn
                    rn = rn+1
                endif
            enddo
            r(iy, ix) = r(iy, ix)/rn
        enddo
    enddo

end subroutine point ! }}}



subroutine iterate(n, m, Vin, maxDiff, Vout)
  implicit none

  integer, intent(in) :: n, m
  double precision, dimension(n, m), intent(in) :: Vin
  double precision, intent(in) :: maxDiff
  double precision, dimension(n, m), intent(out) :: Vout

  double precision, dimension(n, m) :: V, Vold
  integer :: i, j, coun
  
  coun = 0

  V = Vin

  iterationLoop: do

     coun = coun + 1
     Vold = V

     do i=2,n-1
        do j=2, m-1
           V(i, j) = 0.25*(V(i-1,j) + V(i+1, j) + V(i, j-1) + V(i, j+1))
        end do
     end do

     ! Abbruch-Kriterium erreicht?
     if(all(abs(Vold - V) < maxDiff)) then
        exit
     endif
     print *, "Iteration", coun
  end do iterationLoop

  Vout = V

end subroutine iterate

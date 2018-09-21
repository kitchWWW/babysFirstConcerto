\version "2.18.2"
		
#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 20)

\paper{
  indent = 2\cm
  left-margin = 1.5\cm
  right-margin = 1.5\cm
  top-margin = 2\cm
  bottom-margin = 1.5\cm
  ragged-last-bottom = ##f
  ragged-bottom = ##f
max-systems-per-page=4

}


\header{
title ="Baby's First Concerto"
subtitle="
%time
"

composer = "Brian Ellis"
tagline =""
}
\score{
\midi {}
\layout {
  \context {
    \PianoStaff
    \consists #Span_stem_engraver
  }
}

{

 <<
    \new Staff \with{
  midiInstrument = "Celesta"
		fontSize = #-3
		\override StaffSymbol.staff-space = #(magstep -3)
		\override StaffSymbol.thickness = #(magstep -3)
	}\absolute {
%clef
%key
%part2
\bar "|."
	}
    
\new PianoStaff <<
    \new Staff \absolute {
%key
	\tempo 4=80
%part0
    }
    \new Staff \absolute {
%key
      \clef bass
      \voiceOne
      \autoBeamOff
      \crossStaff {
%part1
	  }
    }
  >>


  >>







  }
}
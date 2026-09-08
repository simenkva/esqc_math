
This text accompanies the [[Mathematics.canvas|Mathematics]] canvas. 

Each box contains one field, or topic, and they are connected to other boxes with the arrow indicating the direction from "more general" to "less general and more special". Click headings in this canvas to go to relevant sections in this note.

**NOTE: The arrows are not prerequisites and should not be interpreted as a recommended order of study.**

Of course, many more arrows could be drawn, and many more boxes could be added.  In order to make the graph not too cluttered and confusing, we keep only main links. Additionally, some arrows' direction could be disputed.

## Ranking mathematical topics for quantum chemistry

In the canvas, we rank mathematical topics according to how important they are for understanding and working with quantum chemistry. Let us explain what we mean, since interpreting the rankings wrongly can give the wrong impression of what knowledge is needed.

The ranking refers primarily to **conceptual understanding and the ability to apply mathematical results**, rather than to formal mathematical mastery. A quantum chemist will usually need to understand what a theorem, construction, or mathematical object means and how it can be used, but will much less often need to reproduce its formal proof, or derive new results.

+ ★ : **Core knowledge.** Mathematical concepts and techniques that every working quantum chemist should understand and be able to use. Formal mastery is not implied. Instead, the emphasis is on understanding the main ideas, interpreting the relevant mathematical objects and results, and applying them correctly in quantum-chemical contexts.

+ ◆ : **Valuable knowledge.** Mathematics that a quantum chemist should ideally be familiar with and recognize when encountered. Some working knowledge is valuable, particularly for understanding the theoretical foundations of quantum chemistry and navigating more mathematically oriented literature, but detailed technical knowledge is usually not required.

+ ◇ : **Specialized knowledge.** Mathematics that is not generally needed in quantum chemistry, but that can become useful or important in particular areas or specializations. Most quantum chemists need not study these topics systematically, if at all.

Topics **not marked** are included primarily to place the other subjects in context of the broader mathematical landscape. They are interesting and important areas of mathematics, but have comparatively little direct relevance to most quantum-chemical work.


## Logic and Set Theory ◆

Logic is the branch of mathematics and philosophy that deals with reasoning, the principles of valid inference, and the structure of propositions, i.e., mathematical statements. It provides the formal framework used to analyze and construct mathematical proofs, ensuring that conclusions follow from premises in a valid and systematic way.

Set theory is the branch of mathematics that studies sets, which are collections of objects. In set theory, everything is a set. It forms the foundation for much (all?) of modern mathematics, providing the language and basic concepts used to describe and analyze mathematical structures. Set theory forms the foundation in the sense that every other mathematical theory can be formalized in the language of set theory.

Most mathematicians are aware of formal set theory, but the "version" used in most contexts is "naive set theory", which in a more informal manner defines mathematical sets compared to the rigorous axiom based constructions. As Russel's Paradox shows us, naive set theory has some pitfalls. Most mathematicians simply avoid these pitfalls and stick to naive set theory.

Although formal set theory is unlikely to be applied in the study of quantum chemistry, the basic notation is widely-used and an important language tool when specifying computational methods and their implementation. 

Recommended reading:

>[!book] An Introduction to Proofs with Set Theory by Ashlock and Lee
>![[Pasted image 20240829092150.png|300]]
>Springer (2020)
>https://link.springer.com/book/10.1007/978-3-031-02426-9
>
>A in introduction to logic, set theory, and mathematical proofs for the undergraduate student. Highly recommended!
>
>A link to the set theory chapter available online: https://www.math.uh.edu/~dlabate/settheory_Ashlock.pdf

>[!book] "Set Theory for the Working Mathematician" by Krzysztof Ciesielski
> ![[Pasted image 20240829091657.png]]
> 
> A more advanced text.
> 
> Cambridge University Press (1997) https://doi.org/10.1017/CBO9781139173131



## Category Theory

Category theory is a branch of mathematics that provides a high-level, abstract framework for describing and analyzing mathematical structures and their relationships. It was developed in the 1940s by Samuel Eilenberg and Saunders Mac Lane, and has found applications across nearly all areas of mathematics, as well as in computer science, logic, and theoretical physics.

One of the useful aspects of category theory is that it gives a rigorous language for comparing different mathematical concepts and structures, such as groups and vector spaces.

Although direct use of category theory in quantum chemistry is rare, it is mentioned here as an important branch of modern mathematics.

Recommended reading:
>[!book] A Gentle Introduction to Category Theory by Maarten Fokkinga
>A set of lecture notes. Link to PDF on the author's web site:
>https://maartenfokkinga.github.io/utwente/mmf92b.pdf



## Discrete Mathematics ◇

Lorem ipsum ...
Recommended reading:
>[!book] Concrete Mathematics by Donald Knuth
>![[Pasted image 20240829093357.png]]
>Addison-Wesley (1994)
>
>A classic textbook.
>
>https://en.wikipedia.org/wiki/Concrete_Mathematics
>https://web.archive.org/web/20201106232418/http://www-cs-faculty.stanford.edu/~knuth/gkp.html
>
>

>[!book] Introduction to Graph Theory by Douglas B. West
>![[Pasted image 20240829094014.png|300]]
>
>Link to full book (only for preview): https://daiwz.net/course/disc_math/2023/West_Intro_Graph_Theory_en.pdf
>


## Abstract Algebra ◇

In abstract algebra, sets are given _mathematical structure_ through operations and axioms that define structures such as _groups_, _rings_, and _fields_. A group, for example, is defined in terms of its essential properties rather than any particular concrete realization. Thus, the group $\mathbb{Z}_4 = {0,1,2,3}$ under addition modulo 4 has the same abstract group structure as the matrix group generated by the matrix $\begin{bmatrix}0 & 1 \ -1 & 0\end{bmatrix}$.

Important algebraic structures include groups, semigroups, rings, fields, modules, vector spaces, and algebras. Abstract algebra studies their properties, the relationships between them, and the mappings that preserve their structure.

Abstract algebra is important for quantum chemistry because it provides part of the mathematical foundation for linear algebra, one of the most important tools in the physical sciences, as well as for the study of groups and molecular symmetries. Most quantum chemists do not need a broad command of abstract algebra, but its language and basic ideas provide useful context for many of the mathematical structures encountered in quantum theory.

Recommended reading:
>[!book] A First Course in Abstract Algebra by John B. Fraleigh
>Seventh Edition, Pearson (2003)
>![[Screenshot 2024-08-29 at 09.49.31.png|300]]
>Archived book: https://archive.org/details/firstcourseinabs07edfral

## Elementary Group Theory ★

Group theory is the mathematical study of symmetry. A *group* consists of a set of objects or operations together with a rule for combining them. Important elementary concepts include subgroups, group actions, conjugacy classes, and finite groups.

In chemistry, group theory provides the natural language for describing molecular symmetry. A _point group_ comprises the symmetry operations of a molecule. 

Every quantum chemist should be familiar with the basic language of groups and molecular point groups. The linear-algebraic description of symmetry is the subject of **Representation Theory**.

Recommended reading:

>[!book] Group Theory and Chemistry by David M. Bishop
>![[Pasted image 20240829095053.png|300]]
>Dover (1973)
>
>A classic textbook, very useful.
>
>Link to PDF for preview:  https://library.navoiy-uni.uz/files/david%20m.%20bishop%20-%20group%20theory%20and%20chemistry%20(revised%20edition)(1993)(294s).pdf
>

## Representation Theory ◆

Representation theory studies how abstract groups can be represented by linear transformations, or equivalently by matrices acting on vector spaces. It therefore provides an important connection between **Group Theory** and **Linear Algebra**. A central idea is to decompose a representation into simpler building blocks called *irreducible representations*.

Representation theory is the mathematical machinery underlying much of the practical use of symmetry in quantum chemistry. Molecular orbitals, vibrational modes, and electronic states can be classified according to irreducible representations of molecular point groups. Characters and character tables provide an efficient way of performing this classification, while direct-product representations are useful for determining whether matrix elements vanish by symmetry and for deriving spectroscopic selection rules.

A quantum chemist should be able to understand and use irreducible representations, characters, character tables, and direct products. A deeper understanding of representation theory is valuable for understanding why these tools work and becomes increasingly important in more theoretical treatments of symmetry and angular momentum.

Recommended reading, in addition to the Bishop book mentioned in [[Mathematics Roadmap#Elementary Group Theory ★|Elementary Group Theory ★]] :

>[!book] *Representation Theory: A First Course* by William Fulton and Joe Harris
>Springer, Graduate Texts in Mathematics
>
>![[Screenshot 2026-09-08 at 15.31.31.png|300]]
>
>A classic mathematical introduction to representation theory, with many examples. It begins with representations and characters of finite groups before proceeding to Lie groups and Lie algebras. More advanced and abstract than is normally required for quantum chemistry.

## Lie Groups ◇

A *Lie group* is a group that is also a differentiable manifold, so that its group operations vary smoothly. Lie groups therefore combine ideas from **Group Theory**, **Linear Algebra**, and **Differential Geometry**. Associated with every Lie group is a *Lie algebra*, which describes the infinitesimal transformations generated by the group. Matrix exponentials provide an important connection between Lie algebras and Lie groups.

Lie groups describe continuous symmetries in physics. Of particular importance are the rotation group $SO(3)$ and the closely related group $SU(2)$, which play fundamental roles in the mathematical description of angular momentum and spin. Unitary groups also arise naturally when considering transformations of quantum states and orbitals.

A systematic knowledge of Lie theory is not required for most quantum-chemical work, but it provides a powerful framework for understanding continuous symmetries, angular momentum, unitary transformations, and the geometry of quantum-mechanical state spaces. It becomes particularly useful in more mathematically oriented areas of quantum chemistry and theoretical physics.

Recommended reading:

>[!book] *Lie Groups, Lie Algebras, and Representations: An Elementary Introduction* by Brian C. Hall
>Springer, Graduate Texts in Mathematics
> ![[Screenshot 2026-09-08 at 15.35.14.png|300]]
>
>An especially pedagogical and well-regarded introduction to the theory of Lie groups. The development emphasizes matrix Lie groups and requires relatively little differential geometry, making it well suited to readers approaching the subject from linear algebra, quantum mechanics, or mathematical physics.

## Number Systems ★

The axiomatic definition of the natural numbers using set theory is one of the simplest examples of how set theory serves as foundation for mathematics. The natural numbers are again used to define the integers, rational numbers, real numbers, and complex numbers. These sets are of course among the most important mathematical objects in the sciences. The number systems are again examples of algebraic structures: the integers form a group under addition, the real and complex numbers form fields.

Clearly, understanding numbers is essential to any scientific study. On the other hand, for most purposes, intuitive notions about integers, reals, and complex numbers will be sufficient.

Recommended reading:

* See [[#Logic and Set Theory ◆]]



## Topology ◇

Topology is the study of open and closed sets, and the concept of continuity. A topological space is a set together with a collection of subsets called open subsets, and axioms that these have to obey. From this, topological spaces are generated, allowing us to talk about "closeness" of elements in the set. For example, a metric is an example of a structure that gives rise to a particular kind of topology, that formalizes the notion of distance between points.

In topology the notion of sequences and their convergence is made abstract, including the notion of continuous functions. Topological arguments are indispensable for mathematical analysis of partial differential equations.

For quantum chemists, being aware of the various notions of topology is useful to navigate the literature. For example, the convergence of the pseudocontinuum of the FCI method can be formalized with topological notions. As another example, in density-functional theory, what does it mean that two electronic densities are close together? Being able to distinguish different notions of "closeness of densities" is imperative for understanding, say, modes of convergence of SCF iterations.


Recommended reading:
>[!book] Topology by James R. Munkres
>![[Munkres.png|300]]
>
>Pearson (2014)
>
>This is a classic textbook.
>
>Link to PDF (for preview): https://people.math.ethz.ch/~dkosanovic/24-FS/Munkres-Topology.pdf
>

## Measure and Integration ◆

Measure theory develops abstract notions of length, area, volume, etc., and allows to speak about such notions in potentially very abstract spaces. For example, the Dirac delta function is rigorously defined using measure theory. 

The Lebesgue integral is based on the notion of a Borel measure, and generalizes the Riemann integral. With the Lebesgue integral we can integrate many more functions compared to the Riemann integral,  and operations like exchanging limits and integrals or integration variables obey well-defined and simple theorems. The Lebesgue integral is also necessary to define the $L^2$ Hilbert space of quantum mechanics. 

A passing knowledge if measure theory is very useful for the quantum chemist, since much of the language used in mathematical physics relies on these concepts. That being said, detailed theorems are rarely used, except in borderline cases, where apparent paradoxes may arise. In those cases, these paradoxes are resolved by checking the conditions for, say, interchange of limits and integration.

Recommended reading:
>[!book] The Elements of Integration and Lebesgue Measure by Robert G. Bartle
>![[Bartle.png|300]]
>Wiley Classics, 1995
>
>A slim yet classic textbook on measure and integration.


## Distribution Theory ◆

With distribution theory one extends the concept of functions to include objects, known as _distributions_ or _generalized functions_, which can be used to rigorously define operations like differentiation even for functions that are not classically differentiable. This theory is particularly useful in handling singularities or discontinuities, such as the Dirac delta function, which models an infinitely concentrated point of mass or charge. Distribution theory provides a powerful framework for solving partial differential equations, e.g., using Green's functions.

A rudimentary knowledge of distribution theory is very useful in the study of quantum mechanics. The standard informal view is that "the Dirac delta is a function which is infinite everywhere except at a single point where it is infinity", similarly that "the Green's function is the response of the system to a Dirac delta function", is very useful, but will only take one so far.

Useful in (for example):
- Response theory
- Manybody Green's function theory
- Electromagnetism

Recommended reading:

> [!book] "Mathematical Methods in Physics" by Philippe Blanchard and Erwin Brüning
> 
> ![[Blanchard and Bruening.png|300]]

>[!book] See also the book by [[Recommended General Mathematics Reading#"Mathematical Physics" by Butkov|Butkov]]



## Linear Algebra ★

In linear algebra, one studies linear vector spaces and linear functions between such spaces. Typical, and indeed archetypal, examples are $\mathbb{R}^n$ and $\mathbb{C}^n$, and $n\times m$ matrices with complex or real entries. It is no exaggeration that linear algebra is perhaps the most important tool in science, being at the heart of everything from quantum mechanics, data analysis, and numerical methods for the solution of partial differential equations.

Having a good command of linear algebra is _absolutely essential_ to any theoretical chemist, from the LCAO approach to molecular orbitals, via practical realizations of Kohn--Sham density functional theory, to the numerical solution of, say, the coupled-cluster method.

Recommended reading:

> [!book]  "Linear Algebra Done Right" by Sheldon Axler
> ![[Linear Algebra Done Right.png|300]]
> 
> A highly regarded undergraduate text in linear algebra, considered a very fine piece of didacic writing. Open access. Available for free on the Author's web page: https://linear.axler.net/
> 
  

>[!book] "Introduction to Linear Algebra" by Gilbert Strang
>![[Strang.png|300]]
> A great book by one of the all time greats in linear algebra. See also the [[Recommended YouTube channels]].  
> 
> https://bookstore.ams.org/view?ProductCode=STRANG/5
> 
>

## Multilinear Algebra ◆

In multilinear algebra, linear maps between vector spaces are generalized to maps over several vector spaces to several vector spaces at once, i.e., tensors. Multilinear algebra is rarely taught together with linear algebra, but could well be a subtopic in an advanced course, especially considering it is an important part of modern machine learning methodology. Multilinear algebra finds important use cases in differential geometry, as well as appearing naturally in calculus of several variables. Tensors are also integral to manybody methods like coupled-cluster theory or configuration-interaction theort.

Multilinear algebra is among the more useful topics for quantum chemists.

Recommended reading:

>[!book] "Multilinear Algebra" by Werner Greub
>A springer book on multilinear algebra that I have seen recommended. I have no experience with this book myself.
>
>Springer Verlag.
>Weblink: https://link.springer.com/book/10.1007/978-1-4613-9425-9
>![[Greub.png|300]]


>[!book] "Multilinear Algebra and its Applications"
>Lecture notes: https://www2.math.ethz.ch/education/bachelor/lectures/fs2016/other/mla/ma.pdf 
>
>Course web page at ETH: https://www2.math.ethz.ch/education/bachelor/lectures/fs2016/other/mla.html
>
>The author's name is not disclosed, but the professor that taught the course in 2016 was [Prof. Dr. Özlem Imamoḡlu](https://people.math.ethz.ch/~oezlemi/)


## Calculus ★

Calculus is the branch of mathematics that studies continuous change and is divided into two main areas: differential calculus and integral calculus. Differential calculus focuses on the concept of the derivative, rates of change. Integral calculus, on the other hand, deals with the concept of the integral.

Multivariate calculus extends to functions of several variables, encompassing the study of partial derivatives, multiple integrals, and vector calculus. 

Calculus, together with linear algebra, forms the foundation for much of modern science. It is _absolutely essential_ to have a good grasp of calculus and multivariate calculus for theoretical chemists.

Recommended reading:
>[!book] Vector Calculus by Jerrold E. Marsden and Anthony Tromba
>![[Marsden_frontpage.png|300]]
>

## Complex Analysis ◆

Complex analysis studies the calculus of functions of complex variables. For complex functions, being differentiable is a much more restricting requirement than for real functions, leading to surprising and very strong results of great use in physics and chemistry. Since real functions often are special cases of complex functions, complex analysis is very useful even if complex numbers do not show up at all in a theory.

Useful in: Response theory, quantum dynamics, integral evaluation, perturbation theory, to name a few.

Complex analysis is among the more useful topics for quantum chemists.

Recommended reading:
>[!book] The book by [[Recommended General Mathematics Reading#"Mathematical Physics" by Butkov]] is useful.

>[!book] Complex Analysis by Theodore Gamelin
>![[Pasted image 20240829095847.png|300]]
>Springer (2001).
>
>A very pedagogical textbook.



## Differential Geometry ◇

Differential geometry studies curves, surfaces, and higher-dimensional analogues from an abstract perspective, called differentiable manifolds. These are characterized by the fact that they somehow are smooth, and that locally, i.e., in for sufficiently small neighborhoods of points (if one zooms in on any point), they look like flat space, i.e., $\RR^n$ (or $\CC^n$ for complex manifolds). Thus, differential geometry combines multivariate calculus and linear algebra. One has infinite dimensional versions of the theory, as well, where the modelling spaces are infinite dimensional Banach or Hilbert spaces.

Differential geometry is very useful for abstract understanding of manybody wavefunction methods. For example, the concept of orbital invariance in CASSCF, or the manifold structure of the Hartree-Fock or coupled-cluster methods. See also lie group theory.

Differential geometry is also the foundation for general relativity, and, to a lesser extent, special relativity.

Differential geometry is among the more useful branches of mathematics for quantum chemistry students.

Recommended reading:
>[!book] Geometry of Physics by Theodore Frankel
>![[Pasted image 20240829100049.png]]
>Third Edition, Cambridge University Press (2011)
>A fantastic book.
>Weblink: https://www.cambridge.org/core/books/the-geometry-of-physics/94894F70DB22055BD7BC2B84C135ABAF?pageNum=2&searchWithinIds=94894F70DB22055BD7BC2B84C135ABAF&productType=BOOK_PART&searchWithinIds=94894F70DB22055BD7BC2B84C135ABAF&productType=BOOK_PART&sort=mtdMetadata.bookPartMeta._mtdPositionSortable%3Aasc&pageSize=30&template=cambridge-core%2Fbook%2Fcontents%2Flistings&ignoreExclusions=true

>[!book] Fundamentals of Differential Geometry by Serge Lang
>![[Pasted image 20240829100530.png|300]]
>Springer (1999)
>A classic texbook.
>https://link.springer.com/book/10.1007/978-1-4612-0541-8
>

>[!book]  Differential Geometry of Curves and Surfaces by Manfredo do Carmo
>![[Pasted image 20240829100909.png|300]]
>Prentice-Hall (1976)
>
>A gentle introduction to differential geometry, mostly sticking to familiar Euclidean space.
>
>Link to PDF (for preview): http://www2.ing.unipi.it/griff/files/dC.pdf
>
>do Carmo also has a more advanced book, "Riemannian Geometry"
>![[Pasted image 20240829101030.png|300]]
>Birkhäuser (1992)
>
>Weblink: https://link.springer.com/book/9780817634902
>
>I have used this book sometimes, and it is quite good.
>

>[!book] Manifolds, Tensor Analysis, and Applications by Ralph Abraham, Jerrold E. Marsden, and Tudor Ratiu
>![[Pasted image 20240829164212.png|300]]
>Springer (1988)
>Weblink: https://link.springer.com/book/10.1007/978-1-4612-1029-0
>Archived book: https://archive.org/details/manifoldstensora00abra_0



## Convex Analysis ◇

Convex analysis deals with convex sets and functions. It is an important branch of mathematics, since many optimization problems in science enjoy the property of convexity. Convex analysis introduces a duality transformation, the Legendre-Fenchel transformation, which in many ways are analogous to the Fourier transform.

Convex analysis plays a prominent role in the mathematical foundation of DFT, as pioneered by E.H. Lieb. The Legendre-Fenchel transformation is also important in thermodynamics.

Convex analysis is a useful topic, especially if one wants to study DFT.

Recommended reading:
>[!book] Convex Analysis - An Introductory Text by Jan van Tiel
>![[cover.jpg|300]]
>Wiley (1984)
>
>This is a slim book but highly readable!




## Functional Analysis ◆

Functional analysis can be viewed as infinite dimensional linear algebra. Here, complete normed spaces (Banach spaces) and complete inner product spaces (Hilbert spaces) are studied, along with linear operators between such spaces. Functional analysis is the foundation of quantum mechanics, as done by J. von Neumann. In a way, one can say that the development of functional analysis in the early 20th century was motivated by placing quantum mechanics on rigorous ground.

Functional analysis also provides the mathematical language for abstract treatment of PDEs such as the Schrödinger equation, the Kohn--Sham approach to DFT, Maxwell's equations, and so on.

Functional analysis is a very useful topic for quantum chemists, especially when you want to navigate the more mathematics heavy literature.

Recommended reading:
>[!book] Introductory Functional Analysis with Applications by Erwin Kreyszig
>
> ![[Screenshot 2024-08-29 at 10.15.24.png|300]]


## Fourier Analysis ◆

Fourier analysis studies the representation of functions in terms of oscillating functions of increasing frequency, such as sines, cosines, and complex exponentials. Important concepts include orthogonal expansions, Fourier transforms, convolution, and the extension of Fourier transforms to distributions such as the Dirac delta-function.

Fourier analysis is important throughout physics and quantum chemistry. In quantum mechanics, the position and momentum representations of a wavefunction are related by a Fourier transform. Fourier methods also occur naturally in the analysis and solution of differential equations, in Green’s function methods, and in calculations using plane waves and reciprocal space.

A basic familiarity with Fourier series and Fourier transforms is therefore valuable for quantum chemists. 

>[!book] "Mathematical Physics" by Eugene Butkov, Addison-Wesley Publishing Company (1968)
>
>
> ![[Butkov.png|300]]
While not a rigorous mathematics textbook, this is a classic in mathematical methods for physics courses since its first edition in 1968. You can find [PDFs lying about on the internet](https://edisciplinas.usp.br/pluginfile.php/7270234/mod_folder/content/0/Mathematical%20Physics%20-%20Butkov.pdf). The book is suitable for all students of quantum chemistry, from undergraduate to graduate students.



## Calculus of Variations ★

Calculus of variations deals with the optimization of nonlinear functionals, functions that map _functions_ to scalars. Calculus of variations generalizes vector calculus to infinite dimensions, and as such could also be called "nonlinear functional analysis". Calculus of variations is the correct framework for variational formulations of the laws of nature, from quantum field theory and QED to Hamilton's equations of motion. Moreover, nonlinear approximations to the molecular Schrödinger equation such as Hartree-Fock is naturally formulated in this language.

To have a basic grasp of calculus of variations is almost essential to quantum chemists. A basic knowledge does not require advanced functional analysis, even if the above paragraph gives such an expression.

Calculus of variations is thus an exceedingly important topic in quantum chemistry.

Recommended reading:
- Goldstein, Safko and Poole, "Classical Mechanics"
- Zeidler, "Nonlinear functional analysis"
- ...


## Ordinary Differential Equations ★

Ordinary differential equations (ODEs) describe initial value and boundary value problems of scalar quantities, or coupled such equations. From classical mechanics to rate equations, ODEs permeate theoretical chemistry, and having a basic understanding of essential mathematical results is absolutely essential.

Recommended reading:
* The book by [[Recommended General Mathematics Reading#"Mathematical Physics" by Butkov|Butkov]]


## Dynamical Systems ◇

Dynamical systems theory studies how systems evolve in time according to deterministic rules, typically given by ordinary differential equations or discrete-time mappings. An important aspect of dynamical systems theory is the _qualitative_ and _statistical_ behavior of solutions, rather than concrete solution formulas. Important concepts include phase space, fixed points, stability, periodic orbits, bifurcations, and chaos.

Dynamical systems appear in classical and semiclassical descriptions of molecular motion. Molecular dynamics can be viewed as the evolution of a point through a high-dimensional phase space, and concepts such as stability, conserved quantities, and chaotic behavior are useful for understanding molecular trajectories.

A systematic knowledge of dynamical systems is not required for most quantum chemistry, but the subject becomes useful in molecular dynamics, reaction dynamics, semiclassical methods, and other areas concerned with the time evolution of molecular systems.

Recommended reading:

>[!book] Chaos in Dynamical Systems by Edward Ott
![[s-l1200.jpg|300]]
An entertaining an pedagogical book on chaos and dynamical systems.




## Partial Differential Equations ◆

Partial differential equations (PDEs) generalize ODEs to infinite dimensions, i.e., initial and boundary value problems where the unknown is no longer a scalar or a vector, but an element in a function space. Laws such as Einstein's gravitation theory, transport of heat, chemical reaction-diffusion systems, Maxwell's equations, the various Schrödinger equations, are all PDEs.

PDEs are very important for quantum chemistry.

Recommended reading:
>[!book] Partial Differential Equations by Lawrence C. Evans
> ![[Evans-frontpage.png|300]]
> Second Edition, American Mathematical Society (2010)
> A popular textbook in PDEs.
> Link to PDF (for preview): http://home.ustc.edu.cn/~wclw8181/wffc.files/Partial%20Differential%20Equations.Evans.pdf

>[!book] Functional Analysis, Sobolev Spaces, and Partial Differential Equations by Haim Brezis
>
> ![[Screenshot 2024-08-29 at 16.29.30.png|300]]
>Springer (2011)
> A highly readable book focusing on an abstract framework for PDEs.
> Weblink: https://link.springer.com/book/10.1007/978-0-387-70914-7
  
 

## Operator Algebra ◇

In operator algebra, one studies algebras of operators over linear spaces, often Hilbert spaces. The algebras are often given structures inspired by quantum mechanics, such as canonical anticommutator or canonical commutator relations, e.g. the CAR and CCR algebras. It is a highly abstract branch of pure mathematics, and understanding the basic notions and results may be very useful for the study of manybody theory and quantum field theories.

Recommended reading:

>[!book] Operator Algebras and Quantum Statistical Mechanics by Ola Bratteli and Derek W. Robinson
>![[Pasted image 20240829163631.png|300]]
>Springer (1987)
>A classic textbook, but quite dense, in my opinion.
>Weblink: https://link.springer.com/book/10.1007/978-3-662-02520-8


>[!book] A Course in Operator Theory by John B. Conway
>![[Screenshot 2024-08-30 at 08.41.32.png|300]]
>American Mathematical Society (1999)
>Link: https://bookstore.ams.org/GSM/21
>"This is an excellent course in operator theory and operator algebras ... leads the reader to deep new results and modern research topics ... the author has done more than just write a good book—he has managed to reveal the unspeakable charm of the subject, which is indeed the ‘source of happiness’ for operator theorists."  - _Mathematical Reviews_

>[!book] A list of books for students studying operator algebras
>Link: https://math.vanderbilt.edu/peters10/students.html
>

- See also [[Recommended General Mathematics Reading#"Mathematical Methods in Physics" by Blanchard and Brüning]]







## Probability and Statistics ★

Probability theory provides the mathematical framework for describing random variables, probability distributions, expectation values, correlations, and stochastic processes. Statistics uses probability theory to draw conclusions from data and to quantify uncertainty.

Probability and statistics are increasingly important in quantum chemistry. They are central to Monte Carlo methods, including variational and diffusion Monte Carlo, and to the analysis of stochastic numerical methods. Statistical ideas are also needed for uncertainty quantification, error analysis, fitting models to data, and the interpretation of computational and experimental results. In addition, probability and statistics form part of the mathematical foundation of modern machine learning methods used in chemistry.

At a basic level, a quantum chemist should be comfortable with probability distributions, expectation values, variance and covariance, conditional probability, and elementary statistical estimation. More specialized areas may require stochastic processes, Bayesian methods, Markov chains, and Monte Carlo sampling.

Recommended reading:
* ...


## Information Theory ◇

Information theory provides a mathematical framework for studying information and uncertainty. Central concepts include: entropy, mutual information, measures of correlations between random variables. Classical information theory is therefore closely connected to probability and statistics.

In quantum mechanics, information theoretic ideas generalize from probability distributions to quantum states and density matrices, giving rise to *quantum information theory*. Concepts such as von Neumann entropy, quantum entanglement, and reduced density matrices provide ways of quantifying correlations and information contained in many-particle quantum states.

Information-theoretic ideas occur in quantum chemistry in the analysis of electron correlation and entanglement, particularly in many-body methods such as the density matrix renormalization group and tensor-network approaches. They also provide useful connections between quantum chemistry, quantum computing, statistical mechanics, and modern data analysis.

Recommended reading:

>[!book] *Elements of Information Theory* by Thomas M. Cover and Joy A. Thomas
>Wiley
>
>![[51q29MALXRL._AC_UF1000,1000_QL80_.jpg|300]]
>
>The classic textbook on information theory. A clear and mathematically substantial introduction to entropy, relative entropy, mutual information, information channels, and the connections between information theory, probability, and statistics.

>[!book] *Quantum Computation and Quantum Information* by Michael A. Nielsen and Isaac L. Chuang
>Cambridge University Press
>
> ![[71zJlN985cL._SL1500_.jpg|300]]
>The standard introductory textbook on quantum information and quantum computation. Broad and pedagogical, covering quantum states and operations, entropy and information, entanglement, quantum algorithms, and quantum information theory.



## Numerical Analysis ★

Most equations in quantum chemistry cannot be solved analytically, and must be approximated in finite precision arithmetic on computers. This is the area of numerical analysis. Here, numerical methods for differential equations are studied, as well as numerical linear algebra and eigenvalue finding algorithms, to name some topics.

Numerical analysis is very important for developing and understanding computer implementations of quantum chemistry algorithms.

Recommended reading:
>[!book] Numerical Analysis by Francis B. Hildebrand
>![[Pasted image 20240830084959.png|300]]
>Dover (1956)
>Archived version: https://archive.org/details/introduction_to_numerical_analysis_hildebrand
>
> A classic textbook.

>[!book] Fundamentals of Numerical Computation by Tobin A. Driscoll and Richard J. Braun
>![[Pasted image 20240830085921.png|300]]
>SIAM
>
>A modern textbook of very high quality also available completely for free online. Python, MATLAB, and Julia versions.
>Link: https://tobydriscoll.net/book/fnc/index.html
>Complete book: https://tobydriscoll.net/fnc-julia/frontmatter.html
>


## Optimization and Root Finding ★

Optimization, really a subfield of numerical analysis, deals with finding local or global extremal points of functions of several variables, as well as finding roots of systems of nonlinear equations. There are a multitude of algorithms, such as the method of steepest descent, Newton, and quasi-Newton methods. A very important topic for students of quantum chemistry, as many computational problems end up as an optimization problem.

Recommended reading:
>[!book] Numerical Optimization by Jorge Nocedal and Stephen J. Wright
>![[Screenshot 2024-08-30 at 08.46.35.png|300]]
>Springer (2006)
>Link to PDF (for preview): https://www.math.uci.edu/~qnie/Publications/NumericalOptimization.pdf
>Link: https://link.springer.com/book/10.1007/978-0-387-40065-5
>
> This is an excellent book which I have used a lot.
> 
